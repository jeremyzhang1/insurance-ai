import pytesseract
from PIL import Image

def process_image(file):
    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image)
    return text
