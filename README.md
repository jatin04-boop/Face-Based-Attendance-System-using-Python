# Face-Based Attendance System 👨‍💻📷

A smart and secure attendance system using facial recognition, built with Python. The system features:

* Real-time face recognition using webcam
* Anti-spoofing: head movement and blink detection
* Mask detection to ensure valid attendance
* Buzzer alert for unknown faces
* GUI Dashboard using Tkinter
* Cloud sync to Google Sheets
* Attendance logging in CSV

---

## 🔧 Features

| Feature               | Description                              |
| --------------------- | ---------------------------------------- |
| 🧠 Anti-Spoofing      | Detects eye blinks and head movement     |
| 😷 Mask Detection     | Blocks masked face attendance            |
| 🔔 Unauthorized Alert | Plays buzzer for unknown faces           |
| ☁️ Cloud Sync         | Stores attendance in Google Sheets       |
| 📊 CSV Logs           | Stores attendance locally in a CSV       |
| 🖥️ GUI               | Tkinter GUI dashboard                    |
| 🕒 Smart Camera       | Automatically starts/stops based on time |

---

## 🧰 Tech Stack

* Python
* OpenCV
* dlib / face\_recognition
* Tkinter
* threading
* gspread + Google API (optional)

---

## 📸 Screenshot

<img width="947" alt="Screenshot 2025-04-11 at 1 09 43 PM" src="https://github.com/user-attachments/assets/baeb291f-acb0-4e33-ab9a-f94b02daa309" />

---

## 🚀 How to Run the Face-Based Attendance System

This is a complete guide to set up, run, and use the Face Recognition Attendance System with anti-spoofing features such as blink detection and head movement detection.

### 🧩 Prerequisites

Ensure the following are installed on your system:

* Python 3.7 or higher
* pip (Python package manager)
* A working webcam (internal or external)
* OS: Windows, macOS, or Linux
* Required file: [`shape_predictor_68_face_landmarks.dat`](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) → Place it in the project folder after downloading and extracting

### 📥 1. Clone or Download the Project

Clone this repository:

```bash
git clone https://github.com/yourusername/FaceAttendanceSystem.git
cd FaceAttendanceSystem
```

Or manually download the ZIP and extract it.

### 📦 2. Install Required Python Packages

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python face_recognition dlib numpy pandas Pillow scipy gspread oauth2client
```

### 🧾 3. Project Structure

Make sure your folders look like this:

```
FaceAttendanceSystem/
├── faces/                          # Registered faces saved as images
├── attendance/                     # Attendance logs as Excel/CSV files
├── attendance_system.py            # Main Python GUI script
├── shape_predictor_68_face_landmarks.dat  # Required for facial landmark detection
├── credentials.json                # Google API credentials (optional)
```

✅ `faces/` and `attendance/` folders are auto-created if not present.

### ▶️ 4. Run the Project

Start the application using:

```bash
python attendance_system.py
```

### 🖥️ 5. GUI Controls

After launching, you'll see a GUI with the following buttons:

| Button              | Description                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| **Register Person** | Register a new face. Press `S` to save image, then enter name and roll no. |
| **Delete Person**   | Delete a registered person's image                                         |
| **View Attendance** | Open today's attendance Excel/CSV                                          |
| **Show Registered** | View all registered persons                                                |

### 👁️‍🗨️ 6. How It Works

The system uses your webcam to detect and recognize faces in real-time.

For a person to be marked present:

* Face must match a known face from `faces/`
* Eye blink and head movement (anti-spoofing) must be detected
* No mask should be detected on the face

Once validated:

* Their name is marked in `attendance/attendance_YYYY-MM-DD.xlsx`

### 📌 Notes

* Register faces in well-lit environments for better accuracy.
* Use `Name_RollNo` format when saving names (e.g., `John_101`).
* Anti-spoofing is enforced: static photos or videos won't pass detection.

### 🧼 7. Reset Attendance for New Day

The system automatically logs new attendance each day in a new file. To clear session memory (for repeated testing), restart the app.

---
