## Automated Attendance System with Face Recognition

This is a real-time attendance management system that uses face recognition to automate the attendance tracking process. It allows you to register your face, mark your attendance, and download attendance records.

## Getting Started

Make sure you have the required Python packages installed by running the following command:

```
pip install -r requirements.txt

```
## Usage

1. Register Your Face
    - Run the application: streamlit run app.py
    - Select "Register Face" from the sidebar.
    - Enter your ID and name.
    - Click the "Capture" button to register your face.
    - Your face will be captured using the webcam, saved, and uploaded to Firebase.
2. Mark Attendance
    - Run the application: streamlit run app.py
    - Select "Mark Attendance" from the sidebar.
    - Your face will be captured using the webcam.
    - If recognized and not marked in the last hour, your attendance will be marked.
3. Download Attendance Records
    - Run the application: streamlit run app.py
    - Select "Download Attendance" from the sidebar.
    - You can download the attendance records in CSV format.


## Requirements

Before you can run this project, ensure you have the following software and packages installed:

- [`Python`](https://www.python.org/downloads/): You will need Python 3.7.6 or later version to execute the code.
- [`Firebase Admin SDK`](https://pypi.org/project/firebase-admin/): Required for Firebase integration.
- [`Streamlit`](https://pypi.org/project/streamlit/): Used for creating the web-based interface.
- [`OpenCV Python`](https://pypi.org/project/opencv-python-headless/): Necessary for image and video processing.
- [`Face Recognition`](https://pypi.org/project/face-recognition/): Used for face recognition tasks.


## Note

- The Firebase service account key (serviceAccountKey.json) is essential for Firebase integration and should be placed in the appropriate location.
- The utils directory contains additional Python modules used by the application.



`@Mr Navneet Gupta (navneetguptacse@gmail.com) :: 26 September 2023`
