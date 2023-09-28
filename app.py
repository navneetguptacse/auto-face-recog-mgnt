import streamlit as st
import cv2
import os
import face_recognition
from datetime import datetime
from utils import firebase_utils, image_utils
import base64

firebase_utils.initialize_firebase()

registered_faces = image_utils.load_registered_faces()

def register_face():
    st.subheader("Register Your Face")
    
    user_id = st.text_input("Enter your ID:")
    if not user_id:
        st.warning("Please enter your ID.")
        return

    user_name = st.text_input("Enter your name:")
    if not user_name:
        st.warning("Please enter your name.")
        return

    st.write("Click the 'Capture' button to register your face.")
    if st.button("Capture"):
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        recognized_user_name = image_utils.recognize_face(frame, registered_faces)
        
        if recognized_user_name:
            st.warning(f"Face for {recognized_user_name} is already registered.")
            return
        image_path = f"./data/registered_faces/{user_id}_{user_name}.jpg"
        cv2.imwrite(image_path, frame)
        firebase_utils.upload_image_to_storage(image_path, user_id, user_name)
        firebase_utils.mark_attendance(user_id)
        st.write(f"Face registered for {user_name} (ID: {user_id})")
        video_capture.release()


# Function to download attendance records
def download_attendance():
    st.subheader("Download Attendance Records")
    csv_file_path = firebase_utils.download_attendance_csv()
    if csv_file_path:
        with open(csv_file_path, "rb") as file:
            csv_data = file.read()
        csv_base64 = base64.b64encode(csv_data).decode("utf-8")
        
        href = f'<a href="data:file/csv;base64,{csv_base64}" download="attendance.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No attendance records found.")


# Function to mark attendance
def mark_attendance():
    st.subheader("Mark Attendance")
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    attendance_status = "Not Marked"

    stop_button = st.button("Stop Camera Feed")

    while True:
        
        if face_encodings:
            user_name = image_utils.recognize_face(frame, registered_faces)
            if user_name:
                last_attendance_timestamp = firebase_utils.get_last_attendance_timestamp(user_name)
                if last_attendance_timestamp:
                    last_time = datetime.strptime(last_attendance_timestamp, "%Y-%m-%d %H:%M:%S")
                    current_time = datetime.now()
                    time_difference = (current_time - last_time).total_seconds()
                    if time_difference < 3600:  # 1 hour = 3600 seconds
                        attendance_status = "Already Marked"
                    else:
                        attendance_status = "Marked"
                        firebase_utils.mark_attendance(user_name)
                else:
                    attendance_status = "Marked"
                    firebase_utils.mark_attendance(user_name)
        
        st.image(frame, use_column_width=True, caption="Captured Image")
        st.write(f"Attendance Status: {attendance_status}")
        if stop_button:
            break 
    video_capture.release()


if __name__ == "__main__":
    st.title("Automated Attendance System with Face Recognition")
    sidebar_option = st.sidebar.selectbox("Select an option:", ["Register Face", "Mark Attendance","Download Attendance"])
    
    (register_face() if sidebar_option == "Register Face" else 
    mark_attendance() if sidebar_option == "Mark Attendance" else
    download_attendance() if sidebar_option == "Download Attendance" else None)
 