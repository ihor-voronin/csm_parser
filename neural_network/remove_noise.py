import os
from typing import Tuple

import cv2

from config import Config


# todo: move to image processing
def otsu_threshold(image_folder: str, file_name: str) -> Tuple[str, str]:
    # Load image, grayscale, Otsu's threshold
    image = cv2.imread(f"{image_folder}\\{file_name}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return save_result(thresh, file_name, "otsu_threshold")


    # Invert and apply slight Gaussian blur
    result = 255 - image
    result = cv2.GaussianBlur(result, (3, 3), 0)

    return save_result(result, file_name, "contours_noise")


def save_result(result, file_name: str, method: str) -> Tuple[str, str]:
    base_path_to_save = Config.config()["NeuralNetwork"]["pre_processing_path"]
    path_to_save = f"{base_path_to_save}\\{method}"
    file_path = f"{path_to_save}\\{file_name}"
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    cv2.imwrite(file_path, result)
    return path_to_save, file_name

