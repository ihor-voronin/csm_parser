import os
import shutil
from typing import Dict, List

from settings import Settings
import cv2

from typing import Tuple
from image_processing.load_image import load_image
from image_processing.save_image import save_image, save_result
from image_processing.transform_image import crop, crop_by_solid_color


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


def crop_free_space(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = load_image(f"{image_folder}\\{file_name}")
    thresh = 200
    image = image.convert("L").point(lambda x: 255 if x > thresh else 0, mode="1")
    # image = invert(image)
    # image.show()
    color = image.getpixel((0, 0))
    image = crop_by_solid_color(image=image, color=color)
    # image = expand(image, color=color, border_size=5)
    base_path_to_save = Settings.get_temp_path()
    return save_image(
        image=image, save_folder=f"{base_path_to_save}\\crop", name=file_name
    )


def crop_base_image(image_folder: str, file_name: str) -> Tuple[str, str]:
    image = load_image(f"{image_folder}\\{file_name}")
    width, height = image.size
    crop_to = width - 1
    for x in range(width - 1, 0, -1):
        is_letter = any([image.getpixel((x, y))[0] < 150 for y in range(height)])
        if is_letter:
            crop_to = x
            break
    cropped = crop(
        image,
        0,
        0,
        crop_to + (15 if width - crop_to > 15 else int(width - crop_to / 2)),
        height,
    )

    base_path_to_save = Settings.get_temp_path()
    return save_image(
        image=cropped, save_folder=f"{base_path_to_save}\\crop_base", name=file_name
    )


def otsu_threshold(image_folder: str, file_name: str) -> Tuple[str, str]:
    # Load image, grayscale, Otsu's threshold
    image = cv2.imread(f"{image_folder}\\{file_name}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return save_result(thresh, file_name, "otsu_threshold")


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
