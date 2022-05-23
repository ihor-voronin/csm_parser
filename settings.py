import json
from os import environ
from os.path import join
from typing import Any, Dict, List


class Settings:
    # group WindowConfig
    start_coordinate_x = 0
    start_coordinate_y = 0

    window_width = 1200
    window_height = 700
    window_name: str = "Cyber Station Manager"

    # group PgDn config
    PgDn_contain_nickname = 13

    # group Nickname Page
    page_count: int = None  # type: ignore
    page_start_coordinate_nickname_x = 13
    page_start_coordinate_nickname_y = 255
    page_nickname_width = 600
    page_nickname_height = 28
    page_nickname_count = 200
    page_last_nickname_count: int = None  # type: ignore

    # group Folder
    picture_path: str = join(environ["USERPROFILE"], "Pictures")
    documents_path: str = join(environ["USERPROFILE"], "Documents")

    folder_save_screenshot: str = "CSM_parser_screenshot"
    folder_save_processed: str = "CSM_parser_processed"

    # group NamePattern
    name_pattern: str = "CSM-{name}"

    # group_templates
    templates_is_local: bool = False
    templates_url = "https://raw.githubusercontent.com/ihor-voronin/csm_parser/master/templates.json"
    templates_local_file: str = "templates.json"
    _templates_loaded = None

    # group database
    database_host: str = "localhost"
    database_database: str = "test"
    database_user: str = "root"
    database_password: str = None  # type: ignore

    # group service
    service_name: str = "MySQL"

    # group csv
    csv_output_file_name: str = "output_{timestamp}.csv"
    csv_num_column = "num"
    csv_file_name_column = "file_name"
    csv_nickname_column = "nickname"
    csv_balance_column = "balance"

    @classmethod
    def get_save_screenshot_path(cls) -> str:
        return join(cls.picture_path, cls.folder_save_screenshot)

    @classmethod
    def get_save_processed_path(cls) -> str:
        return join(cls.picture_path, cls.folder_save_processed)

    @classmethod
    def _annotated_variables(cls) -> Dict[str, Any]:
        return cls.__annotations__

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
    def _load_from_dict(cls, payload_dict: dict) -> None:
        class_variables = cls._annotated_variables()
        for key, value in payload_dict.items():
            if key not in class_variables.keys():
                continue
            if not isinstance(value, (class_variables[key],)):
                raise TypeError(f"Incorrect value type for key '{key}'")
            setattr(cls, key, value)
        print(f"New settings for {list(payload_dict.keys())} applied.")

    @classmethod
    def _setting_for_display(cls) -> dict:
        return {
            key: value
            for key, value in cls._class_variables().items()
            if key in cls._annotated_variables().keys()
        }

    @classmethod
    def display_settings(cls) -> None:
        print(
            f"""\nCurrent settings:
            \n{json.dumps(
                cls._setting_for_display(),
                sort_keys=True,
                indent=4,
            )}\n
        """
        )

    @classmethod
    def load_from_string(cls, settings_string: str) -> None:
        try:
            payload_dict = json.loads(settings_string)
        except (TypeError, json.JSONDecodeError):
            raise AttributeError("Incorrect format of settings")
        cls._load_from_dict(payload_dict)

    @classmethod
    def load_from_file(cls, filename: str) -> None:
        with open(filename, "r") as file:
            cls.load_from_string(file.read())

    @classmethod
    def load_from_non_default_args(cls, non_default_args: dict) -> None:
        for key in non_default_args.keys():
            if cls._annotated_variables()[key] is int:
                non_default_args[key] = int(non_default_args[key])
            if cls._annotated_variables()[key] is str:
                non_default_args[key] = str(non_default_args[key])
        cls._load_from_dict(non_default_args)

    @classmethod
    def get_templates(cls) -> List[dict]:
        if cls._templates_loaded is None:
            if cls.templates_is_local:
                from templates import load_templates_from_local_file

                cls._templates_loaded = load_templates_from_local_file(
                    cls.templates_local_file
                )
            from templates import load_templates_from_network

            cls._templates_loaded = load_templates_from_network(cls.templates_url)
        return cls._templates_loaded

    @classmethod
    def _validate_settings(cls, validate_by: dict) -> None:
        is_some_not_set = False
        for key, val in validate_by.items():
            _type = val if val in (int, str, bool) else type(val)
            if not isinstance(getattr(cls, key), (_type,)):
                print(f"Incorrect value type for key '{key}' or not set")
                is_some_not_set = True
        if is_some_not_set:
            raise AttributeError("Not all required attributes applied")

    @classmethod
    def validate_settings(cls) -> None:
        cls._validate_settings(cls._annotated_variables())
        cls._validate_settings(cls._class_variables())
