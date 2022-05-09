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
    window_name = "Discord"

    # group PgDn config
    PgDn_contain_nickname = 13
    PgDn_count_in_full_page = 13
    PgDn_remain_count_nickname = 5
    PgDn_count_in_last_page = 3

    # group Nickname Page
    page_count = 16
    page_start_coordinate_nickname_x = 13
    page_start_coordinate_nickname_y = 255
    page_nickname_width = 600
    page_nickname_height = 28

    # group Folder
    _user_picture_path = join(environ["USERPROFILE"], "Pictures")
    _user_documents_path = join(environ["USERPROFILE"], "Documents")
    _user_temp_path = tempfile.gettempdir()

    folder_save_screenshot = "CSM_parser_screenshot"
    folder_save_processed = "CSM_parser_processed"
    folder_save_temp = "CSM_parser_temp"

    # group NamePattern
    name_pattern = "CSM-{name}-{timestamp}"

    # group_templates
    templates_is_local = False
    templates_url = "https://raw.githubusercontent.com/ihor-voronin/csm_parser/master/templates.json"
    templates_local_file = "templates.json"

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
    def get_save_csv_path(cls) -> str:
        # todo: ~/Documents or from settings var
        return cls._user_documents_path

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
    def display_settings(cls) -> None:
        print(
            f"""\nCurrent settings:
            \n{json.dumps(
                cls._class_variables(),
                sort_keys=True,
                indent=4,
            )}\n
        """
        )

    @classmethod
    def load_from_string(cls, settings_string: str) -> None:
        payload_dict = json.loads(settings_string)
        class_variables = cls._class_variables()
        for key, value in payload_dict.items():
            if key not in class_variables.keys():
                raise AttributeError(f"Incorrect key '{key}'")
            if not isinstance(value, type(class_variables[key])):
                raise TypeError(f"Incorrect value type for key '{key}'")
            setattr(cls, key, value)
        print(f"New settings for {list(payload_dict.keys())} applied.")

    @classmethod
    def load_from_file(cls, filename: str) -> None:
        with open(filename, "r") as file:
            cls.load_from_string(file.read())
