from typing import Any, Dict, List

from image_processing.load_image import load_image
from image_processing.recognize_letter_from_template import (
    recognize_letter_from_template,
)
from image_processing.split_image_into_letters import split_image_into_letter
from load_templates import load_templates
from os_interaction import file_list
from progress_bar import progress_bar
from settings import Settings


def recognize_from_templates() -> List[Dict[str, Any]]:
    image_folder = Settings.get_save_processed_path()

    image_names = file_list(image_folder)

    templates = load_templates()

    count_images = len(image_names)
    result = []
    progress_bar(0, count_images, prefix="Progress:", suffix="Complete", length=50)
    for image_num, image_name in enumerate(image_names, start=1):

        image = load_image(f"{image_folder}\\{image_name}")

        # split image by symbol
        letters = split_image_into_letter(image)

        text = ""
        for letter in letters:
            text += recognize_letter_from_template(letter, templates)

        result.append({"num": image_num, "file_name": image_name, "nickname": text})
        progress_bar(
            image_num, count_images, prefix="Progress:", suffix="Complete", length=50
        )

    return result
