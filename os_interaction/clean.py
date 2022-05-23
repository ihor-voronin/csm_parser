from progress_bar import progress_bar
from settings import Settings

from .folders import delete_folder


def clean_folders() -> None:
    print("Delete folders with images ...")
    image_folders = [
        Settings.get_save_screenshot_path(),
        Settings.get_save_processed_path(),
    ]
    progress_bar(0, len(image_folders))
    for num, image_folder in enumerate(image_folders, start=1):
        delete_folder(image_folder)
        progress_bar(num, len(image_folders))
    print("All used folders removed.")
