from PIL import Image

from os_interaction import file_list, is_folder_exist
from progress_bar import progress_bar
from settings import Settings

from .crop_methods import crop_black_border, crop_by_color_level
from .save_load_image import load_image, save_image
from .threshold_remove import otsu_threshold


def process_single_image(image: Image.Image) -> Image.Image:
    image = crop_by_color_level(image, 150)
    image = otsu_threshold(image)
    return crop_black_border(image)


def prepare_images_for_recognize() -> None:
    print("Prepare nicknames for recognizing")
    base_image_path = Settings.get_save_screenshot_path()
    # create folder if not exists
    is_folder_exist(base_image_path, raise_exception=True)

    files = file_list(base_image_path, raise_exception=True)

    count_images = len(files)

    progress_bar(0, count_images)
    for image_num, base_image_name in enumerate(files, start=1):
        progress_bar(image_num, count_images)
        save_image(
            process_single_image(load_image(f"{base_image_path}/{base_image_name}")),
            Settings.get_save_processed_path(),
            base_image_name,
        )

    print(f"{count_images} image prepared for recognising.")
