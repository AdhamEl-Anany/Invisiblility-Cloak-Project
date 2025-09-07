"""
========================================================
Invisibility Cloak (OpenCV + Python)
========================================================

This project creates an "invisibility cloak" effect using 
OpenCV. The program detects a cloak of a chosen color 
(red, blue, or green) and replaces that region with a 
captured or static background, making the cloak appear 
transparent.

--------------------------------------------------------
Features:
- Works with red, blue, or green cloak colors.
- Supports live background capture or static image.
- Cleans the mask with morphological operations.
- Removes small areas like hands to avoid accidental erasing.
- On-screen usage instructions.
- Adjustable camera resolution and mirror effect.

--------------------------------------------------------
How it Works:
1. Capture a background (live or static image).
2. Convert each video frame from BGR → HSV.
3. Create a mask for the selected cloak color.
4. Clean mask using morphological transformations.
5. Remove small objects to prevent hand detection.
6. Replace cloak region with background.
7. Combine with rest of the frame for final effect.

--------------------------------------------------------
Controls:
- 'b' → Capture background (if not using static image).
- '1' → Set cloak color to red.
- '2' → Set cloak color to blue.
- '3' → Set cloak color to green.
- 'q' → Quit program.

--------------------------------------------------------
Requirements:
- Python 3.x
- OpenCV (cv2)
- NumPy

Install dependencies:
    pip install opencv-python numpy

Run:
    python harrry.py

--------------------------------------------------------
Notes:
- Works best in good lighting with a solid-colored cloak.
- Avoid wearing other items of the same cloak color.
- Resolution defaults to 640x480 for smooth performance.
========================================================
"""

import cv2, sys, numpy as np

#User options:

MIRROR = True           
WIN_NAME = "Invisibility Magic"
CURRENT_COLOR = "red"    
USE_BACKGROUND_IMAGE = False  
BACKGROUND_IMAGE_PATH = "background.jpg"  

#Capture the camera:

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
if not cap.isOpened():
    print("Could not open /dev/video0. Close other apps using camera and try again.")
    sys.exit(1)

#Camera resolution:

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Upload a static background(optional):

background = None
if USE_BACKGROUND_IMAGE:
    background = cv2.imread(BACKGROUND_IMAGE_PATH)
    if background is None:
        print("Could not load background image. Check the path.")
        USE_BACKGROUND_IMAGE = False
    else:
        background = cv2.resize(background, (640, 480))

#Create mask for cloak color:

def get_cloak_mask(hsv, color):
    if color == 'red':
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)
    elif color == 'blue':
        lower = np.array([94, 80, 2])
        upper = np.array([126, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color == 'green':
        lower = np.array([36, 50, 70])
        upper = np.array([89, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    else:
        mask = np.zeros_like(hsv[:,:,0])

    #Clean the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    mask = cv2.dilate(mask, np.ones((5,5), np.uint8), iterations=2)

    #Remove small areas (like hand)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean_mask = np.zeros_like(mask)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > 1500:  # Keep only large areas (cloak)
            clean_mask[labels == i] = 255
    return clean_mask


#Set font and print usage instructions:

font = cv2.FONT_HERSHEY_SIMPLEX


print("Instructions:")
print("1. If using live background, stand out of frame and press 'b' to capture background.")
print("2. Press 1=red, 2=blue, 3=green to choose cloak color.")
print("3. Press 'q' to quit.")

#main loop:

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame.")
        break
    if MIRROR:
        frame = cv2.flip(frame, 1)

    display = frame.copy()
    cv2.putText(display, "[b] capture background  [1] red  [2] blue  [3] green  [q] quit",
                (10, 30), font, 0.6, (200,200,200), 2, cv2.LINE_AA)
    #if background not yet captured:
    if background is None:
        cv2.putText(display, "Step 1: Clear frame, then press 'b' to capture background",
                    (10, 60), font, 0.6, (0,200,200), 2, cv2.LINE_AA)
        cv2.imshow(WIN_NAME, display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            for _ in range(20): #capture several frames
                ret, bg = cap.read()
                if not ret:
                    continue
                if MIRROR:
                    bg = cv2.flip(bg, 1)
            background = bg.copy()
            cv2.putText(display, "Background captured", (10, 90), font, 0.6, (0,200,0), 2, cv2.LINE_AA)
            cv2.imshow(WIN_NAME, display)
            cv2.waitKey(300)
        elif key in (ord('1'), ord('2'), ord('3')):
            CURRENT_COLOR = {'1':'red','2':'blue','3':'green'}[chr(key)]
        continue

    #Apply invisibility effect by replacing cloak area with background    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = get_cloak_mask(hsv, CURRENT_COLOR)
    mask_inv = cv2.bitwise_not(mask)

    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    visible_body = cv2.bitwise_and(frame, frame, mask=mask_inv)
    output = cv2.add(cloak_area, visible_body)

    cv2.putText(output, f"Cloak color: {CURRENT_COLOR}", (10,60), font, 0.6, (0,255,255),2,cv2.LINE_AA)
    cv2.imshow(WIN_NAME, output)

    #handle key presses:

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key in (ord('1'), ord('2'), ord('3')):
        CURRENT_COLOR = {'1':'red','2':'blue','3':'green'}[chr(key)]
    elif key == ord('b') and not USE_BACKGROUND_IMAGE: #recapture background:

        for _ in range(20):
            ret, bg = cap.read()
            if not ret:
                continue
            if MIRROR:
                bg = cv2.flip(bg, 1)
        background = bg.copy()

cap.release()
cv2.destroyAllWindows()
