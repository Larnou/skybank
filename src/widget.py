from datetime import datetime

import pandas as pd

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """
    Функция mask_account_card принимает на вход номер карты или счета и возвращает ее маску.
    :param account_card:
    :return:
    """
    card_digits_part = account_card.split(" ")[-1]
    digits_count = len([char.isdigit() for char in card_digits_part if char.isdigit()])

    if account_card.split(" ")[0].lower() == "счет" and digits_count == 20:
        masked_number = get_mask_account(account_card)
        return masked_number
    elif digits_count == 16:
        masked_number = get_mask_card_number(account_card)
        return masked_number
    else:
        raise ValueError("Проверьте правильность введённых реквизитов карты.")


def get_date(date: str) -> str:
    """
    Функция get_date принимает на вход дату в формате ISO8601 '%Y-%m-%dT%H:%M:%S.f' и возвращает
    в формате '%d.%m.%Y'.
    :param date:
    :return:
    """
    # Time-форматы
    date_format = "%d.%m.%Y"
    date_iso_format = "%Y-%m-%dT%H:%M:%S.%f"

    try:
        # Если передан Timestamp
        if isinstance(date, pd.Timestamp):
            return date.strftime(date_format)

        # Если передана строка
        date_iso_format = "%Y-%m-%dT%H:%M:%S.%f"
        date_obj = datetime.strptime(date, date_iso_format)
        return date_obj.strftime(date_format)

    except Exception as e:
        raise ValueError('Проверьте правильность введённой даты.\nФормат должен быть: "%Y-%m-%dT%H:%M:%S.f"') from e
