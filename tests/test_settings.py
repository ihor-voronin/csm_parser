import json
import tempfile
from os.path import join
from typing import Any

import pytest

from settings import Settings


def test_load_from_string_successful() -> None:
    s = Settings()
    new_page_count = 999999
    settings_string = json.dumps({"page_count": new_page_count})
    s.load_from_string(settings_string)
    assert s.page_count == new_page_count


def test_load_from_string_incorrect_type() -> None:
    s = Settings()
    settings_string = json.dumps({"page_count": str(999999)})
    with pytest.raises(TypeError):
        s.load_from_string(settings_string)


def test_load_from_string_incorrect_key() -> None:
    s = Settings()
    settings_string = json.dumps({"page_count_non_existed": 999999})
    s.load_from_string(settings_string)


def test_load_from_file_successful() -> None:
    s = Settings()
    new_page_count = s.page_count + 1
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count": new_page_count}, tfile)
    tfile.flush()
    filename = tfile.name
    s.load_from_file(filename)
    assert s.page_count == new_page_count


def test_load_from_file_incorect_type() -> None:
    s = Settings()
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count": str(999999)}, tfile)
    tfile.flush()
    filename = tfile.name
    with pytest.raises(TypeError):
        s.load_from_file(filename)


def test_load_from_file_incorect_key() -> None:
    s = Settings()
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count_non_existed": 999999}, tfile)
    tfile.flush()
    filename = tfile.name
    s.load_from_file(filename)


def test_get_save_screenshot_path_successful() -> None:
    s = Settings()
    assert s.get_save_screenshot_path() == join(
        s.picture_path, s.folder_save_screenshot
    )


def test_get_save_processed_path_successful() -> None:
    s = Settings()
    assert s.get_save_processed_path() == join(s.picture_path, s.folder_save_processed)


def test_class_variables() -> None:
    s = Settings()
    variables = s._class_variables()
    correct_variable = "start_coordinate_x"
    class_method_variable = s.get_save_screenshot_path.__name__
    private_variable = "_user_picture_path"
    function_name = s.__init__.__name__  # type: ignore
    assert correct_variable in variables.keys()
    assert class_method_variable not in variables.keys()
    assert private_variable not in variables.keys()
    assert function_name not in variables.keys()


def test_display_settings_successful(capsys: Any) -> None:
    s = Settings()
    s.display_settings()
    out, _ = capsys.readouterr()
    variable_keys = s._annotated_variables().keys()
    assert all(variable_key in out for variable_key in variable_keys)
