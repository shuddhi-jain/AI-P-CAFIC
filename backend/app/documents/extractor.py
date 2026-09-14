import io

import pymupdf
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def extract_text_from_pdf(file_content: bytes) -> str:
    document = pymupdf.open(
        stream=file_content,
        filetype="pdf"
    )

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    document.close()

    return "\n".join(pages)


def preprocess_image(image: Image.Image) -> Image.Image:
    # Convert to grayscale
    image = image.convert("L")

    # Upscale image
    width, height = image.size
    image = image.resize(
        (width * 2, height * 2)
    )

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(2.0)

    # Reduce small noise
    image = image.filter(ImageFilter.MedianFilter(size=3))

    return image


def extract_text_from_image(
    file_content: bytes
) -> str:
    image = Image.open(io.BytesIO(file_content))

    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(
        processed_image,
        config="--psm 6"
    )

    return  text
    

def extract_text(file_content: bytes, mime_type: str) -> str:
    if mime_type == "application/pdf":
        return extract_text_from_pdf(file_content)

    if mime_type.startswith("image/"):
       return extract_text_from_image(file_content)

    if mime_type == "text/plain":
        return file_content.decode("utf-8")

    raise ValueError(
        f"Unsupported file type: {mime_type}"
    )