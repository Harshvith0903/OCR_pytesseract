# Extract Text from PDF and Analyze Tags

This project extracts text from a PDF file, specifically focusing on red-highlighted text, and analyzes unique tags found within the extracted content. The results are saved into an Excel file with separate sheets for extracted text and tag counts.

## Features
- Converts PDF pages to images using `pdf2image`
- Extracts red-highlighted text using `OpenCV`
- Performs OCR with `pytesseract`
- Filters and extracts structured text using regex
- Saves extracted text and unique tag occurrences into an Excel file

## Requirements
Make sure you have the following dependencies installed:
```sh
pip install opencv-python pytesseract numpy pandas pdf2image openpyxl
```
Additionally, ensure `Tesseract-OCR` is installed and accessible.

## Usage
1. Place the target PDF in the specified path.
2. Run the script:
   ```sh
   python extract_text_tags.py
   ```
3. The extracted content will be saved as an Excel file with two sheets:
   - `Extracted Text`: Contains extracted text entries.
   - `Tag Counts`: Displays unique tags and their frequencies.

## Output
- The extracted text is stored in `extracted_text.xlsx`
- Temporary image files are cleaned up automatically after processing

## Notes
- Ensure `tesseract` is correctly configured on your system.
- The script processes red-highlighted text efficiently but may require tuning for different color thresholds.

## License
This project is open-source and free to use.
