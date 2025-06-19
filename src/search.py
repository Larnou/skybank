import re
from collections import defaultdict
from src.parser import read_file_from_csv


# data = read_file_from_csv('../data/transactions.csv')

def process_bank_search(data:list[dict], search_line:str) -> list[dict]:
    # Компилируем регулярное выражение с флагом IGNORECASE
    pattern = re.compile(re.escape(search_line), re.IGNORECASE)

    # Фильтруем операции, где описание соответствует шаблону
    result = [operation for operation in data if pattern.search(operation.get("description"))]
    return result

# categories = ['Перевод организации', 'Перевод с карты на карту', 'Открытие вклада']

def process_bank_operations(data:list[dict], categories:list) -> dict:
    """
    Подсчитывает количество операций по категориям с использованием defaultdict.

    Args:
        data: Список операций
        categories: Список категорий для поиска

    Returns:
        Словарь с количеством операций по категориям
    """

    # Инициализируем словарь с нулевыми значениями
    result = defaultdict(int)

    # Компилируем регулярные выражения для всех категорий
    patterns = {
        category: re.compile(rf"\b{re.escape(category)}\b", re.IGNORECASE) for category in categories
    }

    # Подсчитываем операции
    for operation in data:
        description = operation.get("description", "")
        for category, pattern in patterns.items():
            if pattern.search(description):
                result[category] += 1

    # Возвращаем обычный словарь с нулями для отсутствующих категорий
    return {category: result[category] for category in categories}
