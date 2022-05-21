from typing import Tuple

import cv2

from image_processing.load_image import load_image
from image_processing.save_image import save_cv2_image, save_image
from image_processing.transform_image import crop, crop_by_solid_color
from os_interaction import copy_folder, delete_folder, file_list, is_folder_exist
from progress_bar import progress_bar
from settings import Settings


def get_accurate_result(res1: str, res2: str) -> str:
    if any(i in ". ()[]\\/" for i in res2):
        return res1
    return res2


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
    return save_cv2_image(thresh, file_name, "otsu_threshold")


def prepare_nicknames() -> None:
    print("Prepare nicknames for recognizing")
    base_image_path = Settings.get_save_screenshot_path()
    # create folder if not exists
    is_folder_exist(base_image_path, raise_exception=True)

    files = file_list(base_image_path, raise_exception=True)

    count_images = len(files)

    progress_bar(0, count_images, prefix="Progress:", suffix="Complete", length=50)
    for image_num, base_image_name in enumerate(files, start=1):
        progress_bar(
            image_num, count_images, prefix="Progress:", suffix="Complete", length=50
        )
        image_path, image_name = crop_base_image(base_image_path, base_image_name)
        image_path, image_name = otsu_threshold(image_path, image_name)
        image_path, image_name = crop_free_space(image_path, image_name)

    pre_processing_path = Settings.get_temp_path()
    print(f"Move prepared images to {Settings.get_save_processed_path()} ...")
    copy_folder(f"{pre_processing_path}\\crop", Settings.get_save_processed_path())
    print(f"{count_images} image prepared for recognising.")
    # remove folder with temp images
    delete_folder(pre_processing_path)
