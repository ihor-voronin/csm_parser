import csv
from typing import Dict, List


def write_nicknames_to_csv(nicknames: List[Dict[str, str]], output_file_name: str = "output.csv") -> None:
    csv_columns = nicknames[0].keys()

    try:
        with open(output_file_name, "w", encoding='utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(nicknames)
    except IOError:
        print("I/O error")
