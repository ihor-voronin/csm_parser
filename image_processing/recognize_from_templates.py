import json
import os

from image_processing.load_image import load_image
from image_processing.recognize_letter_from_template import (
    recognize_letter_from_template,
)
from image_processing.split_image_into_letters import split_image_into_letter
from progress_bar import progress_bar
from settings import Settings
from write_nicknames import write_nicknames_to_csv


def recognize_from_templates() -> None:
    image_folder = Settings.get_save_processed_path()

    image_names = os.listdir(image_folder)

    # todo: in future - get templates file from settings
    with open("templates.json") as json_file:
        templates = json.load(json_file)

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

    # todo: get result file name from settings
    write_nicknames_to_csv(result)
