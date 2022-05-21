import time
from typing import Tuple

from PIL import Image, UnidentifiedImageError

from os_interaction import create_folder, is_folder_exist
from settings import Settings


def load_image(path: str) -> Image.Image:
    try:
        return Image.open(path)
    except UnidentifiedImageError:
        return Image.new("RGB", (1, 1))


def save_image(image: Image.Image, save_folder: str, name: str) -> Tuple[str, str]:
    if all(char.isdigit() for char in name):
        name = (
            Settings.name_pattern.format(name=name, timestamp=int(time.time())) + ".png"
        )
    path = f"{save_folder}\\{name}"
    if not is_folder_exist(save_folder):
        create_folder(save_folder)
    image.save(path)
    return save_folder, f"{name}"
