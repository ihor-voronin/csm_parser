import os
import shutil
from typing import Dict, List

from neural_network.pre_processing import crop_free_space, crop_base_image
from neural_network.remove_noise import (
    otsu_threshold,
)
from neural_network.tesseract import recognize_image
from settings import Settings


def get_accurate_result(res1: str, res2: str) -> str:
    if any(i in ". ()[]\\/" for i in res2):
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
    base_image_path = Settings.get_save_screenshot_path()
    # create folder if not exists
    if not os.path.exists(base_image_path):
        raise Exception(f"Folder {base_image_path} does not exist")

    files = os.listdir(base_image_path)
    if not files:
        raise Exception(f"Folder {base_image_path} empty")

    for base_image_name in files:

        image_path, image_name = crop_base_image(base_image_path, base_image_name)
        image_path, image_name = otsu_threshold(image_path, image_name)
        image_path, image_name = crop_free_space(image_path, image_name)

        # print(
        #     f"{file:10} - {recognized_nickname_mode_6:15} - {recognized_nickname_mode_8:15}"
        # )
    pre_processing_path = Settings.get_temp_path()
    copy_to_result_folder(
        f"{pre_processing_path}\\crop", Settings.get_save_processed_path()
    )
    # remove folder with temp images
    shutil.rmtree(pre_processing_path)


def recognize() -> List[Dict[str, str]]:
    image_folder = Settings.get_save_processed_path()
    files = os.listdir(image_folder)
    result = []
    for file in files:
        recognized_nickname_mode_6 = recognize_image(
            f"{image_folder}\\{file}", mode=6
        ).replace("\n", "")
        recognized_nickname_mode_8 = recognize_image(
            f"{image_folder}\\{file}", mode=8
        ).replace("\n", "")

        result.append(
            {
                "file_name": file,
                "recognized_data": get_accurate_result(
                    recognized_nickname_mode_6, recognized_nickname_mode_8
                ),
            }
        )
    return result
