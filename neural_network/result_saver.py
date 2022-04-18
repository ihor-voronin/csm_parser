import os
from typing import Tuple

import cv2

from config import Config


def save_result(result, file_name: str, method: str) -> Tuple[str, str]:
    base_path_to_save = Config.config()["NeuralNetwork"]["pre_processing_path"]
    path_to_save = f"{base_path_to_save}\\{method}"
    file_path = f"{path_to_save}\\{file_name}"
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    cv2.imwrite(file_path, result)
    return path_to_save, file_name
