import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import tempfile


def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    text_chunks = []
    images = convert_from_path(pdf_path)

    for image in images:
        text = pytesseract.image_to_string(image)
        text_chunks.append(text)

    return "\n".join(text_chunks).strip()


def extract_text(file_path: str, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError("Unsupported file type")
