import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

def process_image(file):
    if file.filename.endswith('.pdf'):
        return process_pdf(file)
    else:
        return process_direct_image(file)

def process_pdf(file):
    temp_filename = "temp_uploaded.pdf"
    file.save(temp_filename)

    images = convert_from_path(temp_filename)

    #os.remove(temp_filename)

    if images:
            extracted_text = ""
            for image in images:
                extracted_text += pytesseract.image_to_string(image)
            #print(extracted_text)
            return extracted_text

    else:
        raise Exception("Could not convert PDF to image")

def process_direct_image(file):
    image = Image.open(file.stream)
    return pytesseract.image_to_string(image)
