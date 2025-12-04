import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Load transparent spectacle images
glasses_files = ["glasses1.png", "glasses2.png", "glasses3.png", "glasses4.png"]
glasses = []

for file in glasses_files:
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"⚠ '{file}' not found or unreadable. Skipping.")
    else:
        print(f"✅ Loaded {file}, shape = {img.shape}")
        glasses.append(img)

if not glasses:
    print("❌ No valid glasses found. Exiting.")
    exit()

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not accessible.")
    exit()

index = 0  # Index of current glasses

def overlay_transparent(background, overlay, x, y, overlay_size=None):
    try:
        bg = background.copy()

        if overlay_size:
            overlay = cv2.resize(overlay, overlay_size, interpolation=cv2.INTER_AREA)

        h, w, _ = overlay.shape
        if y + h > bg.shape[0] or x + w > bg.shape[1] or x < 0 or y < 0:
            return bg  # Prevent out-of-frame errors

        if overlay.shape[2] == 4:
            alpha = overlay[:, :, 3] / 255.0
            for c in range(3):
                bg[y:y+h, x:x+w, c] = (
                    (1 - alpha) * bg[y:y+h, x:x+w, c] + alpha * overlay[:, :, c]
                )
        else:
            bg[y:y+h, x:x+w] = overlay

        return bg
    except Exception as e:
        print(f"Overlay error: {e}")
        return background

print("Press 'n' to change glasses | Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠ Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        # Eye landmarks for positioning
        left_eye = (int(landmarks[33].x * w), int(landmarks[33].y * h))
        right_eye = (int(landmarks[263].x * w), int(landmarks[263].y * h))

        # Same size as before
        glasses_width = int(1.5 * abs(right_eye[0] - left_eye[0]))
        glasses_height = int(glasses_width * 0.5)

        # Move slightly to the right (added +10 pixels)
        x = int(left_eye[0] - 0.25 * glasses_width) + 10   # ✅ shifted right
        y = int(left_eye[1] - 0.5 * glasses_height)

        frame = overlay_transparent(frame, glasses[index], x, y, (glasses_width, glasses_height))

    cv2.imshow("🕶 Virtual Spectacle Try-On", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('n'):
        index = (index + 1) % len(glasses)
        print(f"👓 Switched to: {glasses_files[index]}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
