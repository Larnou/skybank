import pandas as pd


def read_file_from_csv(filename: str) -> list[dict]:
    """
    Чтение csv-файла и его псоледущее преобразование в список словарей с ключами колонками исходного файла.
    Args:
        filename: Путь до загружаемого файла

    Returns: Список словарей с ключами названиями колонок csv-файла.
    """
    csv_data = pd.read_csv(filename, sep=";", encoding="utf-8")
    csv_data = csv_data.dropna(how="all")
    csv_data["date"] = pd.to_datetime(csv_data["date"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    operations = csv_data.to_dict("records")

    return operations


def read_file_from_xlsx(filename: str):
    """
    Чтение xlsx-файла и его псоледущее преобразование в список словарей с ключами колонками исходного файла.
    Args:
        filename: Путь до загружаемого файла

    Returns: Список словарей с ключами названиями колонок csv-файла.
    """
    xlsx_data = pd.read_excel(filename)
    xlsx_data = xlsx_data.dropna(how="all")
    xlsx_data["date"] = pd.to_datetime(xlsx_data["date"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce")
    xlsx_data["amount"] = xlsx_data["amount"].apply(lambda x: int(x))
    operations = xlsx_data.to_dict("records")

    return operations

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # DATA_PATH = os.path.join(BASE_DIR, "data", f"{filename}")
