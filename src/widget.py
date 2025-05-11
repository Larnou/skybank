from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """
    Функция mask_account_card принимает на вход номер карты или счета и возвращает ее маску.
    :param account_card:
    :return:
    """
    if account_card[:4].lower() == "счет":
        masked_number = get_mask_account(account_card)
    else:
        masked_number = get_mask_card_number(account_card)

    return masked_number


def get_date(date: str) -> str:
    """
    Функция get_date принимает на вход дату в формате ISO8601 '%Y-%m-%dT%H:%M:%S.ffffff' и возвращает
    в формате '%d.%m.%Y'.
    :param date:
    :return:
    """
    # Time-форматы
    date_format = "%d.%m.%Y"

    date_isoformat = datetime.fromisoformat(date)
    formated_date = datetime.strftime(date_isoformat, date_format)

    return str(formated_date)
