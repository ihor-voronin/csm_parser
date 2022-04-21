import json
import tempfile
from os import environ
from os.path import join


class Settings:
    # group WindowConfig
    start_coordinate_x = 0
    start_coordinate_y = 0

    window_width = 1200  # todo: from settings
    window_height = 700  # todo: from settings

    # group PgDn config
    PgDn_contain_nickname = 13  # todo: from settings
    PgDn_count_in_full_page = 13  # todo: from settings
    PgDn_remain_count_nickname = 5  # todo: from settings
    PgDn_count_in_last_page = 3  # todo: from settings

    # grop Nickname Page
    page_count = 16  # todo: from settings
    page_start_coordinate_nickname_x = 13  # todo: from settings
    page_start_coordinate_nickname_y = 255  # todo: from settings
    page_nickname_width = 600  # todo: from settings
    page_nickname_height = 28  # todo: from settings

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
    def _class_variables(cls) -> dict:
        return {
            key: value
            for key, value in vars(cls).items()
            if not key.startswith("_")
            and not callable(key)
            and not isinstance(value, (classmethod, staticmethod))
        }

    @classmethod
    def settings_payload(cls) -> str:
        return json.dumps(
            cls._class_variables(),
            sort_keys=True,
            indent=4,
        )
