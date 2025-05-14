# Import necessary libraries
import cv2
import face_recognition
import dlib
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import pandas as pd
import os
import threading
from datetime import datetime
from PIL import Image, ImageTk
from scipy.spatial import distance

# Create required directories if they don't exist
os.makedirs('faces', exist_ok=True)        # Stores registered face images
os.makedirs('attendance', exist_ok=True)   # Stores attendance Excel files

# Constants for anti-spoofing checks
EYE_AR_THRESHOLD = 0.2                     # Minimum eye aspect ratio to consider eyes "open"
HEAD_MOVEMENT_THRESHOLD = 10               # Pixel movement threshold for head movement detection
BLINK_REQUIRED = 2                         # Minimum blinks needed to validate a real person
FRAME_BUFFER = 5                           # Frames to track head position history

# Load dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Make sure this file exists

# Global variables to store face data and session state
attendance_list = set()             # Stores names of people whose attendance is already marked
face_encodings_known = []           # Stores encoded features of registered faces
face_names_known = []               # Stores names of registered persons
user_info = {}                      # Stores metadata like roll numbers
blink_counter = 0                   # Counts eye blinks for spoof check
head_positions = []                 # Stores nose positions for head movement detection
cap = cv2.VideoCapture(0)           # Start webcam capture

# Load all saved faces from the 'faces' directory
def load_faces():
    global face_encodings_known, face_names_known, user_info
    face_encodings_known, face_names_known = [], []
    user_info = {}

    for file in os.listdir('faces'):
        if file.endswith('.jpg'):
            image = face_recognition.load_image_file(f'faces/{file}')
            encodings = face_recognition.face_encodings(image)

            if encodings:
                face_encodings_known.append(encodings[0])
                name = file.split('.')[0]
                face_names_known.append(name)
                user_info[name] = f"Roll No: {len(face_names_known)}"  # Example info

# Check if the detected face is already registered
def is_duplicate_face(face_encoding):
    matches = face_recognition.compare_faces(face_encodings_known, face_encoding, tolerance=0.45)
    return True in matches

# Calculate Eye Aspect Ratio (EAR) for blink detection
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Detect if a person has blinked using facial landmarks
def detect_blink(landmarks):
    global blink_counter
    left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
    right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    ear = (left_ear + right_ear) / 2.0

    if ear < EYE_AR_THRESHOLD:  # Eyes considered closed
        blink_counter += 1

    return blink_counter >= BLINK_REQUIRED

# Detect whether the user's head has moved enough (anti-photo spoofing)
def detect_head_movement(landmarks):
    global head_positions
    nose_tip = (landmarks.part(30).x, landmarks.part(30).y)

    if len(head_positions) < FRAME_BUFFER:
        head_positions.append(nose_tip)
        return False  # Not enough history to check movement

    x_diff = abs(head_positions[0][0] - nose_tip[0])
    y_diff = abs(head_positions[0][1] - nose_tip[1])

    head_positions.pop(0)  # Remove oldest position
    head_positions.append(nose_tip)

    return x_diff > HEAD_MOVEMENT_THRESHOLD or y_diff > HEAD_MOVEMENT_THRESHOLD

# Perform combined spoofing detection (blink + head movement)
def detect_spoof(frame):
    global blink_counter
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if not faces:
        return False

    for face in faces:
        landmarks = predictor(gray, face)
        blink_detected = detect_blink(landmarks)
        movement_detected = detect_head_movement(landmarks)

        if blink_detected and movement_detected:
            blink_counter = 0  # Reset counter after successful verification
            return True  # Real person confirmed

    return False

# Generate today's attendance file path
def get_attendance_file_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return f'attendance/attendance_{today}.xlsx'

# Record the attendance of a person in an Excel file
def mark_attendance(name):
    if name in attendance_list:
        return  # Already marked

    attendance_list.add(name)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = get_attendance_file_path()
    df = pd.DataFrame([[name, timestamp]], columns=['Name', 'Timestamp'])

    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df = pd.concat([df_existing, df], ignore_index=True)

    df.to_excel(file_path, index=False)
    messagebox.showinfo("Attendance", f"{name}'s attendance recorded!")

# Recognize faces and validate them with anti-spoofing
def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(face_encodings_known, face_encoding, tolerance=0.45)
        face_distances = face_recognition.face_distance(face_encodings_known, face_encoding)
        best_match = None if len(face_distances) == 0 else face_names_known[np.argmin(face_distances)]

        if True in matches:
            name = best_match
            roll_number = user_info.get(name, "Unknown")

            if detect_spoof(frame):  # Passed anti-spoof check
                color = (0, 255, 0)  # Green rectangle
                mark_attendance(name)
            else:
                color = (0, 255, 255)  # Yellow: recognized but spoof check failed
        else:
            name, roll_number = "Unknown", ""
            color = (0, 0, 255)  # Red: unknown face

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, roll_number, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    return frame

# Continuously capture frames and update Tkinter GUI
def update_frame():
    global cap
    ret, frame = cap.read()

    if ret:
        frame = recognize_faces(frame)
        frame = cv2.resize(frame, (640, 480))
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.img = img

    canvas.after(10, update_frame)  # Update every 10 ms

# Register a new person by capturing their face
def register_person():
    cap_register = cv2.VideoCapture(0)

    if not cap_register.isOpened():
        messagebox.showerror("Error", "Camera not accessible!")
        return

    while True:
        ret, frame = cap_register.read()
        cv2.imshow('Register - Press "s" to save, "q" to quit', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # Save face
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_frame)

            if not encodings:
                messagebox.showerror("Error", "No face detected! Try again.")
                break

            if is_duplicate_face(encodings[0]):
                messagebox.showerror("Error", "This face is already registered!")
                break

            name = simpledialog.askstring("Input", "Enter Name and Roll Number (e.g. John_101):")
            if name:
                cv2.imwrite(f'faces/{name}.jpg', frame)
                messagebox.showinfo("Success", f"{name} registered successfully!")
                load_faces()
            break

        elif key == ord('q'):  # Quit registration
            break

    cap_register.release()
    cv2.destroyAllWindows()

# Delete a registered person's face image
def delete_person():
    person = simpledialog.askstring("Delete", "Enter Name and Roll Number to delete:")

    if person and os.path.exists(f'faces/{person}.jpg'):
        os.remove(f'faces/{person}.jpg')
        messagebox.showinfo("Deleted", f"{person} deleted successfully!")
        load_faces()
    else:
        messagebox.showerror("Error", "Person not found!")

# Open today's attendance file
def view_last_24_hour_attendance():
    file_path = get_attendance_file_path()

    if os.path.exists(file_path):
        try:
            os.startfile(file_path)  # Windows
        except:
            os.system(f'open {file_path}')  # macOS/Linux
    else:
        messagebox.showerror("Error", "No attendance records found!")

# Show all registered persons in a pop-up window
def show_registered_persons():
    files = [f.split('.')[0] for f in os.listdir('faces') if f.endswith('.jpg')]

    if not files:
        messagebox.showerror("Error", "No registered faces found!")
        return

    window = Toplevel(root)
    window.title("Registered Persons")
    listbox = tk.Listbox(window, height=20, width=50)
    listbox.pack(pady=20)

    for file in files:
        listbox.insert(tk.END, file)

    tk.Button(window, text="Close", command=window.destroy).pack(pady=10)

# Reset attendance list for new session
def take_attendance():
    global attendance_list
    attendance_list = set()

# Clean shutdown for the app and release resources
def on_closing():
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# ====================== GUI SETUP ======================
root = tk.Tk()
root.title("Face Based Attendance System")
root.geometry("900x600")

# Button Panel
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# GUI buttons for each function
#tk.Button(frame_buttons, text="Take Attendance", command=take_attendance, height=2, width=20).pack(pady=5)
tk.Button(frame_buttons, text="Register Person", command=register_person, height=2, width=20).pack(pady=5)
tk.Button(frame_buttons, text="Delete Person", command=delete_person, height=2, width=20).pack(pady=5)
tk.Button(frame_buttons, text="View Attendance", command=view_last_24_hour_attendance, height=2, width=20).pack(pady=5)
tk.Button(frame_buttons, text="Show Registered", command=show_registered_persons, height=2, width=20).pack(pady=5)

# Live Camera Feed on GUI
canvas = tk.Canvas(root, width=640, height=480)
canvas.grid(row=0, column=1, padx=10, pady=10)

# Initialize face data and start camera feed
load_faces()
update_frame()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Launch GUI loop
root.mainloop()
