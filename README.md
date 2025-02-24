# OCR Microservice: Extract Text from Images and PDFs

## Overview
This project extracts text from both **images** and **PDFs**, with a special focus on detecting and processing **red-highlighted text** using OpenCV and Tesseract OCR. It applies **image processing techniques** to enhance OCR accuracy and filter text using **regular expressions**.

---

## Features
- Extract red-highlighted text from **images (PNG, JPG, etc.)** and **PDFs**.
- Uses **Tesseract OCR** for text recognition.
- Filters text using **custom regex patterns**.
- Saves processed images for debugging (optional).

---

## Installation
### **1. Install Required Python Libraries**
Make sure you have Python installed, then run:

```bash
pip install opencv-python pytesseract numpy pdf2image poppler-utils
```

### **2. Install Poppler (Required for PDF Processing)**

#### **For macOS (Homebrew)**
```bash
brew install poppler
```

#### **For Ubuntu/Linux**
```bash
sudo apt install poppler-utils
```

#### **For Windows**
1. Download **Poppler for Windows** from [here](https://github.com/oschwartz10612/poppler-windows/releases).
2. Extract the downloaded folder (e.g., `poppler-23.08.0`).
3. Add `C:\poppler-23.08.0\bin` to your **System Environment Variables**.

Verify the installation by running:
```bash
python -c "from pdf2image import convert_from_path; print('pdf2image is working!')"
```

---

## Usage
### **1. Extract Text from Images**
Run the following script to process an image and extract text from red-highlighted areas:

```bash
python image_text_extraction.py
```

### **2. Extract Text from PDFs**
Run the following script to extract text from red-highlighted text in PDFs:

```bash
python pdf_text_extraction.py
```

---

## How It Works
1. **For Images:**
   - Convert the image to HSV color space.
   - Detect red-highlighted text using color masking.
   - Process the masked area and apply OCR.
   - Extract specific patterns using regex.

2. **For PDFs:**
   - Convert PDF pages into images.
   - Process each page as an image (same as above).
   - Extract and filter text from the images.

---

## Expected Output
If the document contains red-highlighted text in the format `XXXX-XXXX-XXXX-XXXX`, the output will be:

```
Filtered Red Highlighted Text:
ABCD-1234-EFGH-5678
X9YZ-A5B6-C7D8-E0F1
```

---

## Contributing
Feel free to fork this repository, submit issues, or make pull requests to improve this project!

---

## License
This project is licensed under the MIT License. You are free to modify and use it for any purpose.
