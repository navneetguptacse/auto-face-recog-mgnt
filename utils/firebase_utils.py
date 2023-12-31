import csv
import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db, storage

_initialized = False

def initialize_firebase():
    global _initialized
    if not _initialized:
        cred = credentials.Certificate("firebase/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://attendance-auto-fceb6-default-rtdb.firebaseio.com/',
            'storageBucket': 'attendance-auto-fceb6.appspot.com'
        })
        _initialized = True

# Upload an image to Firebase Storage
def upload_image_to_storage(image_path, user_id, user_name):
    bucket = storage.bucket()
    blob = bucket.blob(f'face_images/{user_id}_{user_name}.jpg')
    blob.upload_from_filename(image_path)

# Mark attendance and record the timestamp in Firebase with user ID
def mark_attendance(user_id):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database = db.reference('/')
    database.child('attendance').child(user_id).set(current_time)

# Get the last attendance timestamp for a user with user ID
def get_last_attendance_timestamp(user_id):
    database = db.reference('/')
    timestamp = database.child('attendance').child(user_id).get()
    return timestamp

# Fetch attendance data and generate a CSV file
def download_attendance_csv():
    database = db.reference('/')
    attendance_data = database.child('attendance').get()

    if attendance_data:
        attendance_records = []
        for user_id, timestamp in attendance_data.items():
            attendance_records.append({'User ID': user_id, 'Timestamp': timestamp})
        csv_file_path = 'data/attendance.csv'
        with open(csv_file_path, mode='w', newline='') as csv_file:
            fieldnames = ['User ID', 'Timestamp']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(attendance_records)
        return csv_file_path
    else:
        return None
