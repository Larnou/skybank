import json
from typing import Any


def read_json(filepath: str) -> list[Any] | Any:
    try:
        with open(filepath, encoding='utf8') as f:
            data = json.load(f)

        return data
    except:
        return []
