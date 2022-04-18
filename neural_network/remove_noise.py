from typing import Tuple

import cv2
import numpy as np

from neural_network.result_saver import save_result


def otsu_threshold(image_folder: str, file_name: str) -> Tuple[str, str]:
    # Load image, grayscale, Otsu's threshold
    image = cv2.imread(f"{image_folder}\\{file_name}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return save_result(thresh, file_name, "otsu_threshold")


def morph_remove_noise(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = cv2.imread(f"{image_folder}\\{file_name}")
    # Morph open to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    return save_result(opening, file_name, "morph_noise")


def contours_remove_noise(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = cv2.imread(f"{image_folder}\\{file_name}", cv2.IMREAD_GRAYSCALE)
    # Find contours and remove small noise
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 50:
            cv2.drawContours(image, [c], -1, 0, -1)

    # Invert and apply slight Gaussian blur
    result = 255 - image
    result = cv2.GaussianBlur(result, (3, 3), 0)

    return save_result(result, file_name, "contours_noise")


def remove_background_bu_mask_v1(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = cv2.imread(f"{image_folder}\\{file_name}")
    new_img = ((image >= 230) * 255).astype("uint8")
    return save_result(255 - new_img, file_name, "background_mask_v1")


def remove_background_bu_mask_v2(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = cv2.imread(f"{image_folder}\\{file_name}")
    kernel = np.ones((5, 1), np.uint8)
    new_img2 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return save_result(255 - new_img2, file_name, "background_mask_v2")
