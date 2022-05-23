import csv
import time
from os.path import join
from typing import Any, Dict, List, Optional

from settings import Settings


def write_nicknames_to_csv(
    nicknames: List[Dict[str, Any]], remain_money: Optional[Dict[int, float]] = None
) -> None:
    csv_columns = [
        Settings.csv_num_column,
        Settings.csv_file_name_column,
        Settings.csv_nickname_column,
        Settings.csv_balance_column,
    ]

    file_name = Settings.csv_output_file_name.format(timestamp=int(time.time()))

    file_path = join(
        Settings.documents_path,
        file_name,
    )

    try:
        with open(file_path, "w", encoding="utf8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for nickname_dict in nicknames:
                dict_to_write = nickname_dict.copy()
                if remain_money:
                    dict_to_write.update(
                        {
                            Settings.csv_balance_column: remain_money.get(
                                dict_to_write[Settings.csv_num_column], 0
                            )
                        }
                    )
                writer.writerow(dict_to_write)
        print(f"File {file_name} saved to {Settings.documents_path}")
    except IOError:
        print("I/O error")
