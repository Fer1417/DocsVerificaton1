import pytesseract
import re
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_file(file_path):
    text = ""
    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text

def extract_curp(text):
    curp_pattern = r"[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]{2}" 
    match = re.search(curp_pattern, text)
    return match.group(0) if match else None

def extract_rfc(text):
    rfc_pattern = r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}" 
    match = re.search(rfc_pattern, text)
    return match.group(0) if match else None

def extract_imss(text):
    imss_pattern = r"\b\d{11}\b" 
    match = re.search(imss_pattern, text)
    return match.group(0) if match else None

def validate_document(file_path, user_data):
    text = extract_text_from_file(file_path)

    curp = extract_curp(text)
    rfc = extract_rfc(text)
    imss = extract_imss(text)

    validation = {
        "curp": curp == user_data.get("curp"),
        "rfc": rfc == user_data.get("rfc"),
        "imss": imss == user_data.get("imss")
    }

    return validation, {"curp": curp, "rfc": rfc, "imss": imss}
