import json
from typing import Any


def read_json(filepath: str) -> list[Any] | Any:
    try:
        with open(filepath, encoding='utf8') as f:
            data = json.load(f)

        return data
    except:
        return []


# operations = read_json('../da1ta/operations.json')
# print(json.dumps(operations, indent=4, ensure_ascii=False))