from templates.load import (
    load_templates,
    load_templates_from_local_file,
    load_templates_from_network,
)
from templates.recognize_image import recognize_images_from_folder
from templates.recognize_letter import recognize_letter_from_image

__all__ = [
    "load_templates",
    "load_templates_from_local_file",
    "load_templates_from_network",
    "recognize_letter_from_image",
    "recognize_images_from_folder",
]
