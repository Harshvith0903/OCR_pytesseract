import cv2
import pytesseract
import numpy as np
import re
from pdf2image import convert_from_path
import os

# Path to PDF file
pdf_path = "/Users/harshvith/Downloads/4476-DYAB-6-51-0001_3.pdf"  # Replace with your PDF file path

# Convert PDF pages to images
images = convert_from_path(pdf_path, dpi=300)  # Higher DPI improves OCR accuracy

# Temporary folder to store images
temp_folder = "pdf_pages"
os.makedirs(temp_folder, exist_ok=True)

# Define regex pattern for required text format
pattern = r"\b[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+\b"

# List to store extracted text
all_filtered_text = []

# Process each PDF page
for i, img in enumerate(images):
    image_path = os.path.join(temp_folder, f"page_{i+1}.png")
    img.save(image_path, "PNG")  # Save image for OpenCV processing

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color range for red (two ranges in HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color detection
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2  # Combine both masks

    # Apply mask to extract red-highlighted text
    red_text_only = cv2.bitwise_and(image, image, mask=mask)

    # Convert red-highlighted area to grayscale
    gray = cv2.cvtColor(red_text_only, cv2.COLOR_BGR2GRAY)

    # Apply thresholding for better OCR results
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Save processed image (optional for debugging)
    processed_path = os.path.join(temp_folder, f"processed_page_{i+1}.png")
    cv2.imwrite(processed_path, gray)

    # Perform OCR
    custom_config = "--oem 3 --psm 6"
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

    # Extract matching text using regex
    filtered_text = [line.strip() for line in extracted_text.split("\n") if re.search(pattern, line)]
    all_filtered_text.extend(filtered_text)

# Print extracted text
print("Filtered Red Highlighted Text:")
for text in all_filtered_text:
    print(text)

# Optional: Cleanup temp files
import shutil
shutil.rmtree(temp_folder)
