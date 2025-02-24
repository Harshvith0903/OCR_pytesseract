import cv2
import pytesseract
import numpy as np
import re

image_path = "/Users/harshvith/Desktop/red2.png"  # Replace with your actual image path
image = cv2.imread(image_path)

# Convert image to HSV (Hue, Saturation, Value) color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color range for red (two ranges in HSV)
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Create masks to detect red color
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 + mask2  # Combine both masks to cover full red range

# Apply the mask on the original image
red_text_only = cv2.bitwise_and(image, image, mask=mask)

# Convert the red-highlighted text to grayscale
gray = cv2.cvtColor(red_text_only, cv2.COLOR_BGR2GRAY)

# Apply thresholding to enhance contrast
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Save the processed image for debugging (optional)
cv2.imwrite("processed_red_text.png", gray)

# Perform OCR on the processed image
custom_config = "--oem 3 --psm 6"  # OCR engine and segmentation mode
extracted_text = pytesseract.image_to_string(gray, config=custom_config)

# Define regex pattern for the required format
pattern = r"\b[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+\b"

# Extract matching text using regex
filtered_text = [line.strip() for line in extracted_text.split("\n") if re.search(pattern, line)]

print("Filtered Red Highlighted Text:")
for text in filtered_text:
    print(text)