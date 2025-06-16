import json
from typing import Any


def read_json(filepath: str) -> list[Any] | Any:
    """
    Чтение файла формата JSON.
    :param filepath: Путь до файла.
    :return: Данные файла JSON или пустой список, если произошла ошибка чтения.
    """
    try:
        with open(filepath, encoding="utf8") as f:
            data = json.load(f)

        return data
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, PermissionError, IsADirectoryError):
        return []
