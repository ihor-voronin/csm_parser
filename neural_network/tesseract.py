import cv2
import pytesseract


def recognize_image(image_file: str, mode: int = 6) -> str:
    pytesseract.pytesseract.tesseract_cmd = ""  # deprecated
    image = cv2.imread(image_file)
    return pytesseract.image_to_string(image, lang="eng", config=f"--psm {mode}")
