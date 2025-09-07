
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
