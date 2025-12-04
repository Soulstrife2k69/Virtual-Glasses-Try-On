# Virtual Glasses Try-On (Python + OpenCV + MediaPipe)

A real-time virtual spectacle try-on system using **OpenCV**, **MediaPipe FaceMesh**, and **transparent PNG overlays**.  
The program detects facial landmarks and overlays glasses dynamically on your face using your webcam.

---

## Features

- Real-time face tracking using MediaPipe FaceMesh  
- Transparent PNG glasses overlay  
- Multiple glasses with keyboard switching  
- Accurate scaling based on eye landmarks  
- Works on any webcam  

---

## How It Works

1. MediaPipe FaceMesh detects 468 facial landmarks.
2. Eye coordinates (landmarks 33 and 263) determine scaling.
3. PNG glasses are resized and alpha-blended onto the video feed.
4. Press:
   - `n` → Next glasses
   - `q` → Quit

---

## Project Structure

virtual-glasses-tryon/
│
├── main.py
├── requirements.txt
├── README.md
└── assets/
    ├── glasses1.png
    ├── glasses2.png
    ├── glasses3.png
    └── glasses4.png
    
Description:
Real-time AR-style glasses try-on using Python and OpenCV, powered by MediaPipe face landmark detection.


