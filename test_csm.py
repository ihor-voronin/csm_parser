import json, tempfile

import pytest

from testfixtures import TempDirectory
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

def test_load_from_file_successful():
    s = Settings()
    new_page_count = s.page_count + 1
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count": new_page_count}, tfile)
    tfile.flush()
    filename = tfile.name
    s.load_from_file(filename)
    assert s.page_count == new_page_count

def test_load_from_file_incorect_type():
    s = Settings()
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count": str(s.page_count + 1)}, tfile)
    tfile.flush()
    filename = tfile.name
    with pytest.raises(TypeError):
        s.load_from_file(filename)

def test_load_from_file_incorect_key():
    s = Settings()
    tfile = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    json.dump({"page_count_non_existed": s.page_count + 1}, tfile)
    tfile.flush()
    filename = tfile.name
    with pytest.raises(AttributeError):
        s.load_from_file(filename)