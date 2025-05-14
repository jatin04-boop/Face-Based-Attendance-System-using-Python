# Face-Based-Attendance-System-using-Python
using Python

# Face-Based Attendance System 👨‍💻📷

A smart and secure attendance system using facial recognition, built with Python. The system features:

- Real-time face recognition using webcam
- Anti-spoofing: head movement and blink detection
- Mask detection to ensure valid attendance
- Buzzer alert for unknown faces
- GUI Dashboard using Tkinter
- Cloud sync to Google Sheets
- Attendance logging in CSV

---

## 🔧 Features

| Feature | Description |
|--------|-------------|
| 🧠 Anti-Spoofing | Detects eye blinks and head movement |
| 😷 Mask Detection | Blocks masked face attendance |
| 🔔 Unauthorized Alert | Plays buzzer for unknown faces |
| ☁️ Cloud Sync | Stores attendance in Google Sheets |
| 📊 CSV Logs | Stores attendance locally in a CSV |
| 🖥️ GUI | Tkinter GUI dashboard |
| 🕒 Smart Camera | Automatically starts/stops based on time |

---

## 🧰 Tech Stack

- Python
- OpenCV
- dlib / face_recognition
- Tkinter
- threading
- gspread + Google API (optional)

---

## 📸 screenshot
<img width="947" alt="Screenshot 2025-04-11 at 1 09 43 PM" src="https://github.com/user-attachments/assets/baeb291f-acb0-4e33-ab9a-f94b02daa309" />

🚀 How to Run the Face-Based Attendance System
This is a complete guide to set up, run, and use the Face Recognition Attendance System with anti-spoofing features such as blink detection and head movement detection.

🧩 Prerequisites
Ensure the following are installed on your system:

Python 3.7 or higher

pip (Python package manager)

A working webcam (internal or external)

OS: Windows, macOS, or Linux

Required file: shape_predictor_68_face_landmarks.dat (download from dlib model download and place it in the project folder)

📥 1. Clone or Download the Project
Clone this repository:

bash
Copy
Edit
git clone https://github.com/yourusername/FaceAttendanceSystem.git
cd FaceAttendanceSystem
Or manually download the ZIP and extract it.

📦 2. Install Required Python Packages
Run the following command in your terminal:

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is not available, install manually:

bash
Copy
Edit
pip install opencv-python face_recognition dlib numpy pandas Pillow scipy
🧾 3. Project Structure
Make sure your folders look like this:

graphql
Copy
Edit
FaceAttendanceSystem/
├── faces/                     # Registered faces saved as images
├── attendance/                # Attendance logs as Excel files
├── main.py                    # Main Python GUI script
├── shape_predictor_68_face_landmarks.dat  # Required for facial landmark detection
✅ faces/ and attendance/ folders will be auto-created if not present.

▶️ 4. Run the Project
Start the application using:

bash
Copy
Edit
python main.py
🖥️ 5. GUI Controls
After launching, you'll see a GUI with the following buttons:

Button	Description
Register Person	Register a new face. Press S to save image, then enter name and roll no.
Delete Person	Delete a registered person's image
View Attendance	Open today's attendance Excel file
Show Registered	View all registered persons

👁️‍🗨️ 6. How It Works
The system uses your webcam to detect and recognize faces in real-time.

For a person to be marked present:

Face must match a known face from faces/

Eye blink and head movement (anti-spoofing) must be detected

Once validated:

Their name is marked in attendance/attendance_YYYY-MM-DD.xlsx

📌 Notes
Register faces in well-lit environments for better accuracy.

Use Name_RollNo format when saving names (e.g., John_101).

Anti-spoofing is enforced: static photos or videos won't pass detection.

🧼 7. Reset Attendance for New Day
The system automatically logs new attendance each day in a new file. To clear session memory (for repeated testing), restart the app.
