from typing import Iterator

def filter_by_currency(transactions_list: list[dict], currency: str) -> Iterator[dict]:
    """
    Принимает на вход список словарей, представляющих транзакции, возвращать итератор, который поочередно
    выдает транзакции, где валюта операции соответствует заданной (currency).
    :param transactions_list: Список словарей с информацией по транзакциям.
    :param currency: Валюта, по которой необходимо вывести транзакцию
    :return:
    """
    for transaction in transactions_list:
        if transaction.get('operationAmount').get('currency').get('code') == currency:
            yield transaction

def transaction_descriptions(transactions_list: list[dict]) -> Iterator[str]:
    """
    Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
    :param transactions_list: Список словарей с информацией по транзакциям.
    :return:
    """
    for transaction in transactions_list:
        yield transaction.get('description')


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    :param start: Минимальное значение номера карты.
    :param end: Максимальное значение номера карты.
    :return:
    """
    if start > 0 and stop <= 9999999999999999:
        for i in range(start, stop + 1):
            card_number = str(i).zfill(16)
            groups = [card_number[i:i + 4] for i in range(0, 16, 4)]
            yield " ".join(groups)
    else:
        raise ValueError("Проверьте правильность введённых границ номера карты.")
