import logging
import shutil

from .folders import create_folder, is_folder_exist


def copy_folder(source_folder: str, destination_folder: str) -> None:
    try:
        is_folder_exist(source_folder, raise_exception=True)
    except LookupError as e:
        logging.error(str(e))
        raise e
    create_folder(destination_folder, override_folder=True)
    shutil.copytree(source_folder, destination_folder)
