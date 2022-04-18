import os

from config import Config


def delete_images() -> None:
    image_folder = Config.config()["ImageProcessing"]["path"]
    files = os.listdir(image_folder)
    for file in files:
        os.remove(f"{image_folder}\\{file}")
