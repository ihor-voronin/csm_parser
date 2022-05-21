import cv2
from PIL import Image


def otsu_threshold(image: Image.Image) -> Image.Image:
    # Load image, grayscale, Otsu's threshold
    cv2_image = cv2.numpy.array(image)
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return Image.fromarray(thresh)
