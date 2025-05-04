def get_mask_card_number(card_number: int) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован
    и отображается в формате XXXX XX** **** XXXX, где X — это цифра номера.
    :param card_number:
    :return:
    """
    card_str = str(card_number)
    masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked_number


def get_mask_account(account_number: int) -> str:
    """
    Функция get_mask_account принимает на вход номер счета и возвращает его маску. Номер счета замаскирован
    и отображается в формате **XXXX, где X — это цифра номера.
    :param account_number:
    :return:
    """
    account_str = str(account_number)
    masked_number = f"**{account_str[-4:]}"
    return masked_number
