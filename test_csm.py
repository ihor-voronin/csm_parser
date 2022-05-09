import json

import pytest

from settings import Settings


def test_load_from_string_successful():
    s = Settings()
    new_page_count = s.page_count + 1
    settings_string = json.dumps({"page_count": new_page_count})
    s.load_from_string(settings_string)
    assert s.page_count == new_page_count

def test_load_from_sting_incorect_type():
    s = Settings()
    settings_string = json.dumps({"page_count": str(s.page_count + 1)})
    with pytest.raises(TypeError):
        s.load_from_string(settings_string)

def test_load_from_sting_incorect_key():
    s = Settings()
    settings_string = json.dumps({"page_count_non_existed": s.page_count + 1})
    with pytest.raises(AttributeError):
        s.load_from_string(settings_string)
