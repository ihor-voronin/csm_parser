import os
from typing import List


def file_list(source_folder: str, raise_exception: bool = False) -> List[str]:
    files = os.listdir(source_folder)
    if not files and raise_exception:
        raise LookupError(f"Folder {source_folder} empty")
    return files
