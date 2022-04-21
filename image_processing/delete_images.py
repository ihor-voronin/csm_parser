import shutil

from settings import Settings


def delete_images() -> None:
    image_folders = [
        Settings.get_temp_path(),
        Settings.get_save_screenshot_path(),
        Settings.get_save_processed_path()
    ]
    for image_folder in image_folders:
        try:
            shutil.rmtree(image_folder)
        except FileNotFoundError:
            pass
