from datetime import datetime


def filter_by_state(dict_list: list[dict], state_key: str = 'EXECUTED') -> list[dict]:
    """
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению state_key.
    :param dict_list: Список словарей
    :param state_key: Значение ключа для поиска в dict_list
    :return: отфильтрованный список словарей с ключами равному значению state_key
    """
    executed_list = [dictionary for dictionary in dict_list if dictionary.get("state") == state_key]
    return executed_list


def sort_by_date(dict_list: list[dict], sort_way: str = "DESC") -> list[dict]:
    """
    Функция возвращает новый список, отсортированный по ключу date.
    :param dict_list: Список словарей
    :param sort_way: направление сортировки (изначальное по возрастанию
    :return: отсортированный список словарей по ключу date в порядке sort_way
    """
    # параметры для работы функции
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    sort_direction = True if sort_way == "DESC" else False

    # Сортировка по возрастанию даты
    sorted_list = sorted(dict_list, key=lambda x: datetime.strptime(x["date"], date_format), reverse=sort_direction)

    return sorted_list
