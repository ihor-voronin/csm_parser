import json
import tempfile
from os import environ
from os.path import join


class Settings:
    # group WindowConfig
    start_coordinate_x = 0
    start_coordinate_y = 0

    window_width = 1200
    window_height = 700

    # group PgDn config
    PgDn_contain_nickname = 13
    PgDn_count_in_full_page = 13
    PgDn_remain_count_nickname = 5
    PgDn_count_in_last_page = 3

    # grop Nickname Page
    page_count = 16
    page_start_coordinate_nickname_x = 13
    page_start_coordinate_nickname_y = 255
    page_nickname_width = 600
    page_nickname_height = 28

    # grop Folder
    _user_picture_path = join(environ["USERPROFILE"], "Pictures")
    _user_documents_path = join(environ["USERPROFILE"], "Documents")
    _user_temp_path = tempfile.gettempdir()

    folder_save_screenshot = "CSM_parser_screenshot"
    folder_save_processed = "CSM_parser_processed"
    folder_save_temp = "CSM_parser_temp"

    # grop NamePattern
    name_pattern = "CSM-{name}-{timestamp}"

    @classmethod
    def get_save_screenshot_path(cls) -> str:
        return join(cls._user_picture_path, cls.folder_save_screenshot)

    @classmethod
    def get_temp_path(cls) -> str:
        return join(cls._user_temp_path, cls.folder_save_temp)

    @classmethod
    def get_save_processed_path(cls) -> str:
        return join(cls._user_picture_path, cls.folder_save_processed)

    @classmethod
    def _class_variables(cls) -> dict:
        return {
            key: value
            for key, value in vars(cls).items()
            if not key.startswith("_")
            and not callable(key)
            and not isinstance(value, (classmethod, staticmethod))
        }

    @classmethod
    def settings_json(cls) -> str:
        return json.dumps(
            cls._class_variables(),
            sort_keys=True,
            indent=4,
        )

    @classmethod
    def load_from_json(cls, payload: str) -> None:
        print(payload)
        payload_dict = json.loads(payload)
        class_variables = cls._class_variables()
        for key, value in payload_dict.items():
            if key not in class_variables.keys():
                raise Exception(f"Incorrect key '{key}'")
            if not isinstance(value, type(class_variables[key])):
                raise Exception(f"Incorrect value type for key '{key}'")
            setattr(cls, key, value)
