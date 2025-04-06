import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pdf2image
import io
import requests

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extracting text from each page
    return text

# Extract images from PDF and use pytesseract for OCR
def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]

            image = Image.open(io.BytesIO(img_bytes))
            images.append(image)

            # Use pytesseract to extract text from the image (OCR)
            text_from_image = pytesseract.image_to_string(image)
            print(f"Text from image on page {page_num + 1}:\n{text_from_image}\n")
    return images

# Example usage
pdf_path = "your_pdf_file.pdf"

# Extract text
pdf_text = extract_text_from_pdf(pdf_path)
print("Extracted Text:\n", pdf_text)

# Extract images
extracted_images = extract_images_from_pdf(pdf_path)
print(f"Extracted {len(extracted_images)} images from the PDF.")
