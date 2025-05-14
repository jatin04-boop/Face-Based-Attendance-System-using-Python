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

## ▶️ How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/FaceAttendanceSystem.git
cd FaceAttendanceSystem
