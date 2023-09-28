import face_recognition
import os

# Load registered faces and their encodings
def load_registered_faces():
    registered_faces = []
    for file in os.listdir("data/registered_faces"):
        if file.endswith(".jpg"):
            user_name = file.split(".")[0]
            image_path = f"data/registered_faces/{file}"
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                face_encoding = face_encodings[0]
                registered_faces.append((user_name, face_encoding))

    return registered_faces

# Recognize a face in a captured image
def recognize_face(frame, registered_faces):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    recognized_user_name = None
    if not face_encodings:
        return None
    for (user_name, registered_face_encoding) in registered_faces:
        results = face_recognition.compare_faces([registered_face_encoding], face_encodings[0])
        if results[0]:
            recognized_user_name = user_name
            break
    return recognized_user_name
