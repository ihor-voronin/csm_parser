import logging
import os
import shutil


def is_folder_exist(folder_path: str, raise_exception: bool = False) -> bool:
    is_exist = os.path.exists(folder_path)
    if is_exist:
        return True
    if raise_exception and not is_exist:
        raise LookupError(f"Folder {folder_path} does not exist")
    return False


def create_folder(folder_path: str, override_folder: bool = False) -> None:
    try:
        if is_folder_exist(folder_path):
            if override_folder:
                shutil.rmtree(folder_path)
            else:
                return None
    except LookupError as e:
        logging.error(str(e))
        raise e
    os.makedirs(folder_path)


def delete_folder(folder_path: str) -> None:
    try:
        if is_folder_exist(folder_path):
            shutil.rmtree(folder_path)
    except LookupError as e:
        logging.error(str(e))
        raise e
