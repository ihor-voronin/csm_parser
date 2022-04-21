import os
import shutil

from typing import Tuple
from config import Config
from image_processing.load_image import load_image
from image_processing.save_image import save_image
from image_processing.transform_image import crop, crop_by_solid_color
from neural_network.remove_noise import (
    otsu_threshold,
)
from neural_network.tesseract import recognize_image

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


def crop_free_space(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = load_image(f"{image_folder}\\{file_name}")
    thresh = 200
    image = image.convert('L').point(lambda x: 255 if x > thresh else 0, mode='1')
    # image = invert(image)
    # image.show()
    color = image.getpixel((0, 0))
    image = crop_by_solid_color(image=image, color=color)
    # image = expand(image, color=color, border_size=5)
    base_path_to_save = Config.config()["ImageProcessing"]["pre_processing_path"]
    return save_image(
        image=image, save_folder=f"{base_path_to_save}\\crop", name=file_name
    )


def crop_base_image(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = load_image(f"{image_folder}\\{file_name}")
    width, height = image.size
    crop_to = width - 1
    for x in range(width - 1, 0, -1):
        is_letter = any(
            [
                image.getpixel((x, y))[0] < 150
                for y in range(height)
            ]
        )
        if is_letter:
            crop_to = x
            break
    cropped = crop(image, 0, 0, crop_to + (15 if width - crop_to > 15 else int(width - crop_to / 2)), height)

    base_path_to_save = Config.config()["ImageProcessing"]["pre_processing_path"]
    return save_image(
        image=cropped, save_folder=f"{base_path_to_save}\\crop_base", name=file_name
    )


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


        # image_path, image_name = remove_background_bu_mask_v1(
        #     image_path, image_name
        # )
        # image_path, image_name = remove_background_bu_mask_v2(
        #     image_path, image_name
        # )
        # image_path, image_name = morph_remove_noise(
        #     image_path, image_name
        # )
        # image_path, image_name = contours_remove_noise(
        #     image_path, image_name
        # )
        # image_path, image_name = rescale(image_path, image_name)

        # print(
        #     f"{file:10} - {recognized_nickname_mode_6:15} - {recognized_nickname_mode_8:15}"
        # )
    pre_processing_path = Config.config()['ImageProcessing']['pre_processing_path']
    copy_to_result_folder(f"{pre_processing_path}\\crop",
                          Config.config()["ImageProcessing"]["result_path"])
    # remove folder with temp images
    # shutil.rmtree(pre_processing_path)

