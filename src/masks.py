from src.utils import create_logger


masks_logger = create_logger('masks_logger', 'masks')

def get_mask_card_number(card_number: str) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован
    и отображается в формате XXXX XX** **** XXXX, где X — это цифра номера.
    :param card_number: Номер карты.
    :return:
    """

    card_digits_part = card_number.split(" ")[-1]
    digits_count = len([char.isdigit() for char in card_digits_part if char.isdigit()])
    masks_logger.info(f'Получен следующий номер карты {card_digits_part}.')

    if digits_count == 16 and len(card_digits_part) == 16:
        masks_logger.info(f'Номер карты {card_digits_part} введён правильно.')
        masked_number = f"{card_number[:-12]} {card_number[-12:-10]}** **** {card_number[-4:]}"
        masks_logger.info(f'Результат маскирования {masked_number}.')
        return masked_number
    else:
        error_message = 'Проверьте правильность введённого номера карты.'
        masks_logger.error(error_message)
        raise ValueError(error_message)


def get_mask_account(account_number: str) -> str:
    """
    Функция get_mask_account принимает на вход номер счета и возвращает его маску. Номер счета замаскирован
    и отображается в формате **XXXX, где X — это цифра номера.
    :param account_number:
    :return:
    """

    card_digits_part = account_number.split(" ")[-1]
    digits_count = len([char.isdigit() for char in card_digits_part if char.isdigit()])
    masks_logger.info(f'Получен следующий номер счёта {account_number}.')

    if digits_count == 20 and len(card_digits_part) == 20:
        masks_logger.info(f'Номер счёта {card_digits_part} введён правильно.')
        masked_number = f"{account_number[:4]} **{account_number[-4:]}"
        masks_logger.info(f'Результат маскирования {masked_number}.')
        return masked_number
    else:
        error_message = "Проверьте правильность введённого номера счёта."
        masks_logger.error(error_message)
        raise ValueError(error_message)
