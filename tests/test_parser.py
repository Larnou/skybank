import pandas as pd
import pytest

from src.parser import read_file_from_csv, read_file_from_xlsx


def test_csv_successful_read_and_conversion(mock_read_csv):
    """Тест успешного чтения и преобразования данных"""
    # 1. Создаем реальный DataFrame вместо MagicMock
    data = {
        "date": ["2023-01-01T12:00:00Z", "2023-02-01T15:30:00Z"],
        "amount": [100, 200],
        "description": ["Payment", "Transfer"],
    }
    mock_df = pd.DataFrame(data)
    mock_read_csv.return_value = mock_df

    # 2. Вызов функции
    result = read_file_from_csv("test.csv")

    # 3. Проверки
    mock_read_csv.assert_called_once_with("test.csv", sep=";", encoding="utf-8")
    assert len(result) == 2
    assert result[0]["amount"] == 100
    assert str(result[0]["date"]) == "2023-01-01 12:00:00"
    assert result[1]["description"] == "Transfer"


def test_csv_file_not_found_handling(mock_read_csv):
    """Тест обработки отсутствия файла"""
    mock_read_csv.side_effect = FileNotFoundError("File not found")

    with pytest.raises(FileNotFoundError):
        read_file_from_csv("non_existent.csv")


def test_csv_invalid_dates_handling(mock_read_csv):
    """Тест обработки невалидных дат"""
    # Подготовка данных с невалидной датой
    test_data = [
        {"date": "2023-01-01T12:00:00Z", "amount": 100},
        {"date": "INVALID_DATE", "amount": 200},
        {"date": "2023-13-01T00:00:00Z", "amount": 300},
    ]
    mock_df = pd.DataFrame(test_data)
    mock_read_csv.return_value = mock_df

    result = read_file_from_csv("invalid_dates.csv")

    # Проверяем валидную дату
    assert isinstance(result[0]["date"], pd.Timestamp)
    assert str(result[0]["date"]) == "2023-01-01 12:00:00"

    # Проверяем невалидные даты
    assert pd.isna(result[1]["date"])  # Проверяем NaT для 'INVALID_DATE'
    assert pd.isna(result[2]["date"])  # Проверяем NaT для несуществующей даты


def test_xlsx_successful_read_and_conversion(mock_read_excel):
    """Тест успешного чтения и преобразования данных из XLSX"""
    # 1. Подготовка тестовых данных
    test_data = [
        {"date": "2023-01-01T12:00:00Z", "amount": 150.0, "description": "Salary"},
        {"date": "2023-01-05T18:30:00Z", "amount": -75.5, "description": "Grocery"},
    ]
    mock_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = mock_df

    # 2. Вызов функции
    result = read_file_from_xlsx("test.xlsx")

    # 3. Проверки
    mock_read_excel.assert_called_once_with("test.xlsx")
    assert len(result) == 2
    assert result[0]["amount"] == 150.0
    assert result[1]["description"] == "Grocery"
    assert str(result[0]["date"]) == "2023-01-01 12:00:00"
    assert str(result[1]["date"]) == "2023-01-05 18:30:00"


def test_xlsx_invalid_dates_handling(mock_read_excel):
    """Тест обработки невалидных дат в XLSX"""
    # 1. Подготовка данных с невалидной датой
    test_data = [
        {"date": "2023-01-01T12:00:00Z", "amount": 100},
        {"date": "INVALID_DATE", "amount": 200},
        {"date": "2023-13-01T00:00:00Z", "amount": 300},
    ]
    mock_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = mock_df

    # 2. Вызов функции
    result = read_file_from_xlsx("invalid_dates.xlsx")

    # 3. Проверки
    assert isinstance(result[0]["date"], pd.Timestamp)
    assert pd.isna(result[1]["date"])
    assert pd.isna(result[2]["date"])


def test_xlsx_file_not_found_handling(mock_read_excel):
    """Тест обработки отсутствия XLSX-файла"""
    # 1. Настройка выброса исключения
    mock_read_excel.side_effect = FileNotFoundError("File not found")

    # 2. Проверка выброса исключения
    with pytest.raises(FileNotFoundError):
        read_file_from_xlsx("non_existent.xlsx")
