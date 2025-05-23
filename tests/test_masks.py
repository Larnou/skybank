import pytest

from src.masks import get_mask_account, get_mask_card_number

# Тестирование правильности маскирования номера карты.
# Проверка работы функции на различных входных форматах номеров карт, включая граничные случаи и
# нестандартные длины номеров.
# Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты.


@pytest.mark.parametrize(
    "card_number",
    [
        "Platinum 22202345612340099",
        "Maestro 1234",
        "Visa 1234 5678",
        "Maestro abc123",
        "Maestro",
        "",
    ],
)
def test_get_masks_card_number_quantity(card_number):
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(card_number)
    assert str(exc_info.value) == "Проверьте правильность введённого номера карты."


@pytest.mark.parametrize(
    "card_number_example, card_number_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Mastercard 4800195634128604", "Mastercard 4800 19** **** 8604"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number(card_number_example, card_number_result):
    assert get_mask_card_number(card_number_example) == card_number_result


# Тестирование правильности маскирования номера счета.
# Проверка работы функции с различными форматами и длинами номеров счетов.
# Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины.


@pytest.mark.parametrize(
    "account_number",
    [
        "Счет 222023456123400991231231",  # слишком длинный номер
        "Счет 1234231231",  # слишком короткий номер
        "Счет 1234312 567811",  # содержит пробелы
        "Счет abc123!!аав",  # содержит буквы
        "Счет",  # пустой номер
        "",  # пустая строка
        "Счет 73654108430135874305kek",
        "Счет 73654108430135874kek",
    ],
)
def test_get_masks_account_number_quantity(account_number):
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(account_number)
    assert str(exc_info.value) == "Проверьте правильность введённого номера карты."


@pytest.mark.parametrize(
    "account_number_example, account_number_result",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 12345678430135876590", "Счет **6590"),
        ("Счет 56234111241142374125", "Счет **4125"),
    ],
)
def test_get_mask_account(account_number_example, account_number_result):
    assert get_mask_account(account_number_example) == account_number_result
