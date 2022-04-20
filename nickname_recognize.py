import os
import time
from typing import Dict, List
from config import Config
from image_processing.load_image import load_image
from image_processing.transform_image import crop

csv_columns = ["file_name", "recognized_data"]
csv_file = "result.csv"


def get_accurate_result(res1: str, res2: str) -> str:
    if any(i in '. ()[]\\/' for i in res2):
        return res1
    return res2


def copy_to_result_folder(source_folder: str, destination_folder: str) -> None:
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = f"{source_folder}\\{file_name}"
        destination = f"{destination_folder}\\{file_name}"
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)


def prepare_nicknames() -> None:
    base_image_path = Config.config()["ImageProcessing"]["path"]
    # create folder if not exists
    if not os.path.exists(base_image_path):
        os.makedirs(base_image_path)

    files = os.listdir(base_image_path)
    # img = load_image(r"Q:\PyProjects\WinShellControll\test-00232-1649948029.png")
    #
    # colors = []
    # width, height = img.size
    # for x in range(width):
    #     for y in range(height):
    #         colors.append(img.getpixel((x, y))[0])
    # print(min(colors))

    for base_image_name in files:

        image_path, image_name = crop_base_image(base_image_path, base_image_name)
        image_path, image_name = otsu_threshold(image_path, image_name)
        image_path, image_name = crop_free_space(image_path, image_name)

