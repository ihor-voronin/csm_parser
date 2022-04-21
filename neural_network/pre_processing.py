from typing import Tuple


from image_processing.load_image import load_image
from image_processing.save_image import save_image
from image_processing.transform_image import (
    crop_by_solid_color,
    crop,
)
from settings import Settings


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
