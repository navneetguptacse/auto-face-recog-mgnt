import streamlit as st
import cv2
import os
import face_recognition
from datetime import datetime
from utils import firebase_utils, image_utils
import base64

# Initialize Firebase
firebase_utils.initialize_firebase()

# Load registered faces
registered_faces = image_utils.load_registered_faces()

# Function to register a user's face
def register_face():
    st.subheader("Register Your Face")
    
    # Prompt the user to enter their ID (required)
    user_id = st.text_input("Enter your ID:")
    
    if not user_id:
        st.warning("Please enter your ID.")
        return
    
    # Prompt the user to enter their name (required)
    user_name = st.text_input("Enter your name:")
    
    if not user_name:
        st.warning("Please enter your name.")
        return
    
    st.write("Click the 'Capture' button to register your face.")
    
    if st.button("Capture"):
        # Access the webcam and capture an image
        video_capture = cv2.VideoCapture(1)
        ret, frame = video_capture.read()
        
        # Perform face recognition to check if the face is already registered
        recognized_user_name = image_utils.recognize_face(frame, registered_faces)
        
        if recognized_user_name:
            st.warning(f"Face for {recognized_user_name} is already registered.")
            return
        
        # Save the captured image with user ID in the filename
        image_path = f"./data/registered_faces/{user_id}_{user_name}.jpg"
        cv2.imwrite(image_path, frame)
        
        # Upload the image to Firebase Storage with user ID in the filename
        firebase_utils.upload_image_to_storage(image_path, user_id, user_name)
        
        # Mark attendance in Firebase with user ID
        firebase_utils.mark_attendance(user_id)
        
        st.write(f"Face registered for {user_name} (ID: {user_id})")
        video_capture.release()


# Function to download attendance records
def download_attendance():
    st.subheader("Download Attendance Records")
    
    csv_file_path = firebase_utils.download_attendance_csv()
    if csv_file_path:
        # Open the CSV file and read its contents
        with open(csv_file_path, "rb") as file:
            csv_data = file.read()
        
        # Encode the CSV data as base64
        csv_base64 = base64.b64encode(csv_data).decode("utf-8")
        
        # Create a download link
        href = f'<a href="data:file/csv;base64,{csv_base64}" download="attendance.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No attendance records found.")


# Function to mark attendance
def mark_attendance():
    st.subheader("Mark Attendance")
    
    # Access the webcam and capture an image
    video_capture = cv2.VideoCapture(1)
    ret, frame = video_capture.read()
    
    # Find faces in the captured image
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    # Initialize attendance status
    attendance_status = "Not Marked"
    
    if face_encodings:
        # Recognize the captured face
        user_name = image_utils.recognize_face(frame, registered_faces)
        
        if user_name:
            # Check if the user has already marked attendance in the last hour
            last_attendance_timestamp = firebase_utils.get_last_attendance_timestamp(user_name)
            if last_attendance_timestamp:
                last_time = datetime.strptime(last_attendance_timestamp, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()
                time_difference = (current_time - last_time).total_seconds()
                if time_difference < 30:  # 1 hour = 3600 seconds
                    attendance_status = "Already Marked"
                else:
                    attendance_status = "Marked"
                    firebase_utils.mark_attendance(user_name)
            else:
                attendance_status = "Marked"
                firebase_utils.mark_attendance(user_name)
    
    st.image(frame, use_column_width=True, caption="Captured Image")
    st.write(f"Attendance Status: {attendance_status}")
    
    video_capture.release()


if __name__ == "__main__":
    st.title("Automated Attendance System with Face Recognition")
    sidebar_option = st.sidebar.selectbox("Select an option:", ["Register Face", "Mark Attendance","Download Attendance"])
    
    if sidebar_option == "Register Face":
        register_face()
    elif sidebar_option == "Mark Attendance":
        mark_attendance()
    elif sidebar_option == "Download Attendance":
        download_attendance()