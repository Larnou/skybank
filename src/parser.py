from datetime import datetime

import pandas as pd

def read_file_from_csv(filename: str) ->list[dict]:
    """
    Чтение csv-файла и его псоледущее преобразование в список словарей с ключами колонками исходного файла.
    Args:
        filename: Путь до загружаемого файла

    Returns: Список словарей с ключами названиями колонок csv-файла.
    """
    csv_data = pd.read_csv(filename, sep=';', encoding='utf-8')
    csv_data['date'] = pd.to_datetime(csv_data['date'], format='%Y-%m-%dT%H:%M:%SZ')
    operations = csv_data.to_dict('records')

    return operations


def read_file_from_xlsx(filename: str):
    """
    Чтение xlsx-файла и его псоледущее преобразование в список словарей с ключами колонками исходного файла.
    Args:
        filename: Путь до загружаемого файла

    Returns: Список словарей с ключами названиями колонок csv-файла.
    """
    xlsx_data = pd.read_excel(filename)
    xlsx_data['date'] = pd.to_datetime(xlsx_data['date'], format='%Y-%m-%dT%H:%M:%SZ')
    operations = xlsx_data.to_dict('records')

    return operations
