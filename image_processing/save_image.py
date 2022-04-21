import os
import time
from typing import Tuple

import cv2
from numpy import ndarray
from PIL import Image

from settings import Settings


def save_image(image: Image.Image, save_folder: str, name: str) -> Tuple[str, str]:
    if all(char.isdigit() for char in name):
        name = (
            Settings.name_pattern.format(name=name, timestamp=int(time.time())) + ".png"
        )
    path = f"{save_folder}\\{name}"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    image.save(path)
    # print(f'image {name} saved')
    return save_folder, f"{name}"


def save_cv2_image(result: ndarray, file_name: str, method: str) -> Tuple[str, str]:
    base_path_to_save = Settings.get_temp_path()
    path_to_save = f"{base_path_to_save}\\{method}"
    file_path = f"{path_to_save}\\{file_name}"
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    cv2.imwrite(file_path, result)
    return path_to_save, file_name
