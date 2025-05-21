def get_mask_card_number(card_number: str) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован
    и отображается в формате XXXX XX** **** XXXX, где X — это цифра номера.
    :param card_number:
    :return:
    """

    card_digits_part = card_number.split(' ')[-1]
    digits_count = len([char.isdigit() for char in card_digits_part if char.isdigit()])

    if digits_count == 16 and len(card_digits_part) == 16:
        masked_number = f"{card_number[:-12]} {card_number[-12:-10]}** **** {card_number[-4:]}"
        return masked_number
    else:
        raise ValueError('Проверьте правильность введённого номера карты.')


def get_mask_account(account_number: str) -> str:
    """
    Функция get_mask_account принимает на вход номер счета и возвращает его маску. Номер счета замаскирован
    и отображается в формате **XXXX, где X — это цифра номера.
    :param account_number:
    :return:
    """

    card_digits_part = account_number.split(' ')[-1]
    digits_count = len([char.isdigit() for char in card_digits_part if char.isdigit()])

    if digits_count == 20 and len(card_digits_part) == 20:
        masked_number = f"{account_number[:4]} **{account_number[-4:]}"
        return masked_number
    else:
        raise ValueError('Проверьте правильность введённого номера счёта.')
