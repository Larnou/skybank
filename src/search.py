import re
from collections import defaultdict, Counter

from src.parser import read_file_from_csv


data = read_file_from_csv('../data/transactions.csv')

def process_bank_search(data:list[dict], search_string:str) -> list[dict]:
    """
        Фильтрует список банковских операций по наличию строки в описании.

        Args:
            data: Список словарей с данными операций
            search_string: Строка для поиска в описании операций

        Returns:
            Отфильтрованный список операций, где строка найдена в описании
        """
    # Компилируем регулярное выражение с флагом IGNORECASE
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтруем операции, где описание соответствует шаблону
    result = [operation for operation in data if pattern.search(operation.get("description"))]
    return result



def process_bank_operations(data:list[dict], categories:list) -> dict:
    """
    Подсчитывает количество операций по категориям

    Args:
        data: Список операций
        categories: Список категорий для поиска

    Returns:
        Словарь с количеством операций по категориям
    """

    # Извлекаем все значения description, игнорируя отсутствующие ключи
    descriptions = [operation.get('description') for operation in data]

    # Создаем счетчик и преобразуем в обычный словарь
    counter_dict = dict(Counter(descriptions))

    return {category: counter_dict[category] for category in categories}

# categories = ['Перевод организации', 'Перевод с карты на карту', 'Открытие вклада']
# res = process_bank_operations(data, categories)
# print(res)
