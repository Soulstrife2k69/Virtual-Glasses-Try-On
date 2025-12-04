import cv2

files = ["glasses1.png", "glasses2.png", "glasses3.png"]

for file in files:
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ {file} not loaded.")
    else:
        print(f"✅ {file} loaded successfully. Shape: {img.shape}")
