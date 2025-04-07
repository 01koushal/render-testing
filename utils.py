import PyPDF2
import fitz
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception:
        return None

def extract_images_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        images = []
        for page in doc:
            for img in page.get_images(full=True):
                base_image = doc.extract_image(img[0])
                image_bytes = base_image["image"]
                images.append(Image.open(io.BytesIO(image_bytes)))
        return images
    except:
        return []

def is_image_based_pdf(pdf_path):
    return not extract_text_from_pdf(pdf_path) and bool(extract_images_from_pdf(pdf_path))
