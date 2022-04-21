import os
import time
from typing import Tuple

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
