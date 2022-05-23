from typing import Any, Dict, List

from PIL import Image

from image_processing import load_image, split_image_into_letter
from os_interaction import file_list
from progress_bar import progress_bar
from settings import Settings

from .recognize_letter import recognize_letter_from_image


def recognize_image(image: Image.Image) -> str:
    letters = split_image_into_letter(image)

    text = ""
    for letter in letters:
        text += recognize_letter_from_image(letter, Settings.get_templates())

    return text


def recognize_images_from_folder(folder: str) -> List[Dict[str, Any]]:
    image_names = file_list(folder)

    count_images = len(image_names)
    result = []

    progress_bar(0, count_images)

    for image_num, image_name in enumerate(image_names, start=1):
        image = load_image(f"{folder}\\{image_name}")
        text = recognize_image(image)

        result.append({"num": image_num, "file_name": image_name, "nickname": text})

        progress_bar(image_num, count_images)

    return result
