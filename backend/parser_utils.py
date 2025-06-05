from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(file_bytes):
    text = ""
    reader = PdfReader(io.BytesIO(file_bytes))
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image)

def extract_combined_text(files):
    combined_text = ""
    for file in files:
        content = file.file.read()
        if file.filename.endswith(".pdf"):
            combined_text += extract_text_from_pdf(content) + "\n"
        elif file.filename.endswith((".jpg", ".jpeg", ".png")):
            combined_text += extract_text_from_image(content) + "\n"
    return combined_text
