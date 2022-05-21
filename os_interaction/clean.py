from os_interaction import delete_folder
from progress_bar import progress_bar
from settings import Settings


def clean_folders() -> None:
    print("Delete folders with images ...")
    image_folders = [
        Settings.get_temp_path(),
        Settings.get_save_screenshot_path(),
        Settings.get_save_processed_path(),
    ]
    progress_bar(
        0, len(image_folders), prefix="Progress:", suffix="Complete", length=50
    )
    for num, image_folder in enumerate(image_folders, start=1):
        delete_folder(image_folder)
        progress_bar(
            num, len(image_folders), prefix="Progress:", suffix="Complete", length=50
        )
    print("All used folders removed.")
