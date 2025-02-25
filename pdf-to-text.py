import cv2
import pytesseract
import numpy as np
import re
import pandas as pd
from pdf2image import convert_from_path
import os
import shutil
from openpyxl import load_workbook

# Path to PDF file
pdf_path = '/Users/harshvith/Desktop/Hextasphere/Projects/Optical Character Recognition(OCR)/4476-DYAB-6-51-0001_3.pdf'

# Convert PDF pages to images
images = convert_from_path(pdf_path, dpi=300)

# Temporary folder to store images
temp_folder = "pdf_pages"
os.makedirs(temp_folder, exist_ok=True)

# Define regex pattern for required text format
pattern = r"\b[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+-[A-Za-z0-9]+\b"

# List to store extracted text along with page numbers
extracted_data = []

# Process each PDF page
for page_number, img in enumerate(images, start=1):
    image_path = os.path.join(temp_folder, f"page_{page_number}.png")
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

    # Perform OCR
    custom_config = "--oem 3 --psm 6"
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

    # Extract matching text using regex and ensure each match appears on a new line
    words = extracted_text.split()
    for word in words:
        if re.search(pattern, word):
            extracted_data.append(word)

# Convert extracted data to DataFrame
df = pd.DataFrame(extracted_data, columns=["Extracted Text"])

# Count occurrences of unique tags within the extracted text
tag_pattern = r"\b[A-Z]{2,}\b"
df["Tag"] = df["Extracted Text"].apply(lambda x: re.search(tag_pattern, x).group(0) if re.search(tag_pattern, x) else None)
tag_counts = df["Tag"].value_counts().reset_index()
tag_counts.columns = ["Tag", "Count"]

# Save extracted data and unique tag counts in separate sheets
excel_file_path = "/Users/harshvith/Desktop/Hextasphere/Projects/Optical Character Recognition(OCR)/extracted_text.xlsx"
with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Extracted Text", index=False)
    tag_counts.to_excel(writer, sheet_name="Tag Counts", index=False)

# Adjust column width after saving
wb = load_workbook(excel_file_path)
ws = wb["Extracted Text"]

# Auto-adjust column width for Extracted Text column
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter  # Get the column letter
    for cell in col:
        try:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass
    adjusted_width = max_length + 2
    ws.column_dimensions[col_letter].width = adjusted_width

# Save the workbook again with adjusted column width
wb.save(excel_file_path)

# Cleanup temporary files
shutil.rmtree(temp_folder)

# Provide a message confirming the file save
print(f"\n Extracted text saved to: {excel_file_path}")
