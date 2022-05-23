import json
from typing import List

import requests


def load_templates_from_network(templates_url: str) -> List[dict]:
    resp = requests.get(templates_url)
    return json.loads(resp.text)


def load_templates_from_local_file(templates_local_file: str) -> List[dict]:
    with open(templates_local_file) as json_file:
        templates = json.load(json_file)
    return templates
