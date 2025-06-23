import json
import logging
import os
from pathlib import Path
from typing import Any


def create_logger(logger_name: str, filename: str) -> logging.Logger:
    """
    Создание именованного логгера с записью в указанный файл.
    Автоматически создает директорию для логов, если она не существует.

    :param logger_name: Название логгера
    :param filename: Имя файла логов (без расширения)
    :return: Настроенный логгер
    """
    # 1. Создаем путь к директории логов
    log_dir = Path(__file__).parent.parent / "logs"

    # 2. Создаем директорию, если она не существует
    log_dir.mkdir(parents=True, exist_ok=True)

    # 3. Формируем полный путь к файлу
    log_file = log_dir / f"{filename}.log"

    # 4. Создаем логгер
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 5. Удаляем старые обработчики (предотвращает дублирование)
    if logger.hasHandlers():
        logger.handlers.clear()

    # 6. Создаем обработчик для файла
    file_handler = logging.FileHandler(filename=log_file, mode="w", encoding="utf-8")

    # 7. Настраиваем форматтер
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - module %(filename)s in %(funcName)s: %(message)s")
    file_handler.setFormatter(formatter)

    # 8. Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger


utils_logger = create_logger("utils_logger", "utils")


def read_json(filename: str) -> list[Any] | Any:
    """
    Чтение файла формата JSON.
    :param filename: Путь до файла.
    :return: Данные файла JSON или пустой список, если произошла ошибка чтения.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", f"{filename}")

    try:
        utils_logger.info(f"Попытка открыть файл {filename}")
        with open(DATA_PATH, encoding="utf8") as f:
            data = json.load(f)
        utils_logger.info("Данные файла успешно прочитаны")

        return data
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, PermissionError, IsADirectoryError):
        utils_logger.error("При чтении данных возникла ошибка")
        return []
