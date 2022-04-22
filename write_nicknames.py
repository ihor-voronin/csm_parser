import csv
from os.path import join
from typing import Any, Dict, List

from settings import Settings


def write_nicknames_to_csv(
    nicknames: List[Dict[str, Any]], output_file_name: str = "output.csv"
) -> None:
    csv_columns = nicknames[0].keys()

    file_path = join(Settings.get_save_csv_path(), output_file_name)

    try:
        with open(file_path, "w", encoding="utf8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(nicknames)
        print(f"File {output_file_name} saved to {Settings.get_save_csv_path()}")
    except IOError:
        print("I/O error")
