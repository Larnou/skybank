import json
import logging
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


def create_logger(logger_name, filename):
    """
    Создание именованного логера с записью в определенёый файл.
    :param logger_name: Название именованного логера.
    :param filename: Названия файла, в который будут записаны результаты логирования.
    :return: Именованный логер logger_name
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Основной файл (все сообщения)
    main_handler = logging.FileHandler(filename=f"../logs/{filename}.log", mode='w', encoding='utf-8')

    # Настройка форматтеров
    main_handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s - module %(filename)s in %(funcName)s: %(message)s"
    ))

    # Добавление обработчиков
    logger.addHandler(main_handler)
    return logger