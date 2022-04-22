import json
from typing import List

import requests

from settings import Settings


def load_templates_from_network() -> List[dict]:
    resp = requests.get(Settings.templates_url)
    return json.loads(resp.text)


def load_templates_from_local_file() -> List[dict]:
    with open(Settings.templates_local_file) as json_file:
        templates = json.load(json_file)
    return templates


def load_templates() -> List[dict]:
    if Settings.templates_is_local:
        return load_templates_from_local_file()
    return load_templates_from_network()
