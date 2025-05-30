import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Тестирование генератора card_number_generator:
# Напишите тесты, которые проверяют, что генератор выдает правильные номера карт в заданном диапазоне.
# Проверьте корректность форматирования номеров карт.
# Убедитесь, что генератор корректно обрабатывает крайние значения диапазона и правильно завершает генерацию.

@pytest.mark.parametrize("card_number_start, card_number_stop, card_number_result", [
    (1, 2, ['0000 0000 0000 0001', '0000 0000 0000 0002']),
    (23456, 23457, ['0000 0000 0002 3456', '0000 0000 0002 3457']),
    (12345678, 12345679, ['0000 0000 1234 5678', '0000 0000 1234 5679']),
    (9999999999999998, 9999999999999999, ['9999 9999 9999 9998', '9999 9999 9999 9999'])
])
def test_card_number_generator(card_number_start, card_number_stop, card_number_result):
    result = list(card_number_generator(card_number_start, card_number_stop))
    assert result == card_number_result


def test_card_number_generator_bad_start_value():
    generator = card_number_generator(start=-1, stop=1)
    results = []

    with pytest.raises(ValueError) as exc_info:
        for item in generator:
            results.append(item)

    assert results == []
    assert str(exc_info.value) == 'Проверьте правильность введённых границ номера карты.'


def test_card_number_generator_bad_stop_value():
    generator = card_number_generator(9999999999999998, 10000000000000001)
    results = []

    with pytest.raises(ValueError) as exc_info:
        for item in generator:
            results.append(item)

    assert results == []
    assert str(exc_info.value) == 'Проверьте правильность введённых границ номера карты.'


# Тестирование функции transaction_descriptions:
# Проверьте, что функция возвращает корректные описания для каждой транзакции.
# Тестируйте работу функции с различным количеством входных транзакций, включая пустой список.

def test_transaction_descriptions(list_of_transactions):
    generator_result = [x for x in transaction_descriptions(list_of_transactions)]
    assert generator_result == [
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод со счета на счет',
        'Перевод с карты на карту',
        'Перевод организации'
    ]

def test_transaction_descriptions_doubled(double_list_of_transactions):
    generator_result = [x for x in transaction_descriptions(double_list_of_transactions)]
    assert generator_result == [
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод со счета на счет',
        'Перевод с карты на карту',
        'Перевод организации',
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод со счета на счет',
        'Перевод с карты на карту',
        'Перевод организации'
    ]

def test_transaction_descriptions_empty_list(empty_list_of_transactions):
    generator_result = [x for x in transaction_descriptions(empty_list_of_transactions)]
    assert generator_result == []

# Тестирование функции filter_by_currency:
# Напишите тесты, проверяющие, что функция корректно фильтрует транзакции по заданной валюте.
# Проверьте, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют.
# Убедитесь, что генератор не завершается ошибкой при обработке пустого списка или списка без соответствующих
# валютных операций.

def test_filter_by_currency_usd(list_of_transactions):
    generator_result = [x for x in filter_by_currency(list_of_transactions, "USD")]
    assert generator_result == [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
    ]

def test_filter_by_currency_rub(list_of_transactions):
    generator_result = [x for x in filter_by_currency(list_of_transactions, "RUB")]
    assert generator_result == [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {
                        "amount": "67314.70",
                        "currency": {
                            "name": "руб.",
                            "code": "RUB"
                        }
                    },
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657"
        }
    ]

def test_filter_by_currency_empty_list(empty_list_of_transactions):
    generator_result = [x for x in filter_by_currency(empty_list_of_transactions, "RUB")]
    assert generator_result == []


def test_filter_by_currency_yena(list_of_transactions):
    generator_result = [x for x in filter_by_currency(list_of_transactions, "YENA")]
    assert generator_result == []
