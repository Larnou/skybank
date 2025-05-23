from src.widget import mask_account_card, get_date
import pytest

# Тесты для проверки, что функция корректно распознает и применяет нужный тип маскировки в зависимости от типа входных данных (карта или счет).
# Параметризованные тесты с разными типами карт и счетов для проверки универсальности функции.
# Тестирование функции на обработку некорректных входных данных и проверка ее устойчивости к ошибкам.

@pytest.mark.parametrize("number_example, number_result", [
    ('Visa Platinum 7000792289601234', 'Visa Platinum 7000 79** **** 1234'),
    ('Mastercard 4800195634128604', 'Mastercard 4800 19** **** 8604'),
    ('Maestro 2203792289609000', 'Maestro 2203 79** **** 9000'),
    ('Счет 73654108430135874305', 'Счет **4305'),
    ('Счет 12345678430135876590', 'Счет **6590'),
    ('Счет 56234111241142374125', 'Счет **4125'),
])

def test_mask_account_card(number_example, number_result):
    assert mask_account_card(number_example) == number_result


@pytest.mark.parametrize("bank_account", [
    'Maestro 22037909000',
    'СчЁт 22202345611111100991231231',  # слишком длинный номер
    'Счет 1231231',                     # слишком короткий номер
    'Visa 1234312 567811',              # содержит пробелы
    'Счет abc123!!аав121234567',        # содержит буквы
    'Счет',                             # пустой номер
    '',                                 # пустая строка
])

def test_mask_account_card_value(bank_account):
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(bank_account)
    assert str(exc_info.value) == 'Проверьте правильность введённых реквизитов карты.'

# Тестирование правильности преобразования даты.
# Проверка работы функции на различных входных форматах даты, включая граничные случаи и нестандартные строки с датами.
# Проверка, что функция корректно обрабатывает входные строки, где отсутствует дата.

@pytest.mark.parametrize("date_unformatted, date_formatted", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2021-11-24T04:26:18.914013", "24.11.2021"),
    ("2023-05-04T12:26:18.342123", "04.05.2023"),
])

def test_get_date(date_unformatted, date_formatted):
    assert get_date(date_unformatted) == date_formatted

@pytest.mark.parametrize("uncorrect_data", [
    "2024-34-72T02:26:18.671407",
    "2021-11-24 04:26:18.914013",
    "05-2024-04T12:26:18.342123",
    "05-2024-04T12:26:18",
    "05-2024-04",
    '',
])

def test_get_date_values(uncorrect_data):
    with pytest.raises(ValueError) as exc_info:
        get_date(uncorrect_data)
    assert str(exc_info.value) == 'Проверьте правильность введённой даты.\nФормат должен быть: "%Y-%m-%dT%H:%M:%S.f"'