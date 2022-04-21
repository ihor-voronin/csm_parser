import os
import time
from typing import Tuple

import cv2

from PIL import Image

from config import Config


def save_image(image: Image.Image, save_folder: str, name: str) -> Tuple[str, str]:
    if all(char.isdigit() for char in name):
        name = Config.config()["ImageProcessing"]["name_format"].format(
            name=name, timestamp=int(time.time())
        ) + ".png"
    path = f"{save_folder}\\{name}"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    image.save(path)
    # print(f'image {name} saved')
    return save_folder, f"{name}"


def save_result(result, file_name: str, method: str) -> Tuple[str, str]:
    base_path_to_save = Config.config()["ImageProcessing"]["pre_processing_path"]
    path_to_save = f"{base_path_to_save}\\{method}"
    file_path = f"{path_to_save}\\{file_name}"
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    cv2.imwrite(file_path, result)
    return path_to_save, file_name

