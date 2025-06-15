import pytest
from src.utils import read_json


def test_valid_json_list(tmp_path):
    """Проверка чтения корректного JSON-файла со списком"""
    file_path = tmp_path / "test.json"
    file_path.write_text('[1, 2, 3]', encoding='utf8')

    result = read_json(str(file_path))
    assert result == [1, 2, 3]

def test_valid_json_dict(tmp_path):
    """Проверка чтения корректного JSON-файла со словарем"""
    file_path = tmp_path / "test.json"
    file_path.write_text('{"key": "value"}', encoding='utf8')

    result = read_json(str(file_path))
    assert result == {"key": "value"}

def test_file_not_found():
    """Проверка обработки отсутствующего файла"""
    result = read_json("non_existent_file.json")
    assert result == []

def test_invalid_json(tmp_path):
    """Проверка обработки некорректного JSON"""
    file_path = tmp_path / "test.json"
    file_path.write_text('invalid json', encoding='utf8')

    result = read_json(str(file_path))
    assert result == []

def test_empty_file(tmp_path):
    """Проверка обработки пустого файла"""
    file_path = tmp_path / "test.json"
    file_path.write_text('', encoding='utf8')

    result = read_json(str(file_path))
    assert result == []