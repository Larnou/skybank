from src.generators import filter_by_currency
from src.parser import read_file_from_csv, read_file_from_xlsx
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import read_json
from src.widget import get_date, mask_account_card


def welcome_user(user: str, program: str):
    """
    Функция приветствия пользователя и предложения выбора последующей работы (выбор файла).
    Args:
        user: Пользователь.
        program: Программа.


    Returns: Формат файла для открытия базы транзакций
    """
    print(f"{program}: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")

    menu_variants = {
        1: "1. Получить информацию о транзакциях из JSON-файла",
        2: "2. Получить информацию о транзакциях из CSV-файла",
        3: "3. Получить информацию о транзакциях из XLSX-файла",
    }

    for i in range(1, len(menu_variants) + 1):
        print(menu_variants.get(i))

    user_choice = int(input(f"\n{user}: "))
    program_answer = menu_variants.get(user_choice).split(" ")[-1][:-1]
    print(f"\n{program}: Для обработки выбран {program_answer}.")

    file_type = program_answer.split("-")[0]
    return file_type


def get_filter_status(user: str, program: str):
    """
    Функция статуса транзакции для фильтрации списка транзакций из выбранного файла.
    Args:
        user: Пользователь.
        program: Программа.

    Returns: Статус транзакции для фильтрации по ней.
    """
    status_variants = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print(f"\n{program}: Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(status_variants)}\n")

        user_choice = input(f"{user}: ").upper()
        if user_choice in status_variants:
            print(f'{program}: Операции отфильтрованы по статусу "{user_choice}"')
            return user_choice
        else:
            print(f'\n{program}: Статус операции "{user_choice}" недоступен.')


def get_parameters(user: str, program: str):
    """
    Функция получения допольнительных параметров для фильтрации списка транзакций из выбранного файла.
    Args:
        user: Пользователь.
        program: Программа.

    Returns: Формат файла для открытия базы транзакций
    """
    file_type = welcome_user(user, program)
    filter_status = get_filter_status(user, program)

    # Дополнительные вопросы

    print(f"\n{program}: Отсортировать операции по дате? Да/Нет\n")
    user_choice_datasort = input(f"{user}: ").lower()
    sort_by_date = True if user_choice_datasort == "да" else False

    if sort_by_date:
        print(f"\n{program}: Отсортировать по возрастанию или по убыванию?\n")
        user_choice_sort = input(f"{user}: ").lower()
        sort = True if user_choice_sort in ["возрастанию", "возрастание", "по возрастанию"] else False

    print(f"\n{program}: Выводить только рублевые транзакции? Да/Нет\n")
    user_choice_rub = input(f"{user}: ").lower()
    show_rub_transactions = True if user_choice_rub == "да" else False

    # На данном этапе получены все обязательные ответы, которые содержат ответ.
    parameters = {
        "file_type": file_type,
        "filter_status": filter_status,
        "sort_by_date": sort_by_date,
        "sort": sort,
        "show_rub_transactions": show_rub_transactions,
    }

    print(f"\n{program}: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
    user_choice_filter_description = input(f"{user}: ").lower()
    if user_choice_filter_description == "да":
        print(f"\n{program}: Введите необходимое слово в описании транзакции.\n")
        filter_word = input(f"{user}: ").lower()
        parameters["filter_word"] = filter_word

    return parameters


def print_transaction_info(transaction: dict):
    """
    Вывод информации о транзакции.
    Args:
        transaction: Транзакция.

    Returns: Формат файла для открытия базы транзакций
    """

    date = get_date(transaction.get("date"))
    description = transaction.get("description")
    account_to = mask_account_card(transaction.get("to"))

    # Получаем первый уровень
    operation_amount = transaction.get("operationAmount")

    # Проверяем, что operationAmount существует и является словарём
    if isinstance(operation_amount, dict):
        # Получаем валютный словарь
        currency_dict = operation_amount.get("currency")
        currency = currency_dict.get("name")
        amount = currency_dict.get("amount")
    else:
        currency = "руб." if transaction.get("currency_name") == "Ruble" else transaction.get("currency_name")
        amount = transaction.get("amount")

    print(f"\n{date} {description}")
    if "from" in transaction:
        account_from = mask_account_card(transaction.get("from"))
        print(f"{account_from} -> {account_to}")
    else:
        print(f"{account_to}")
    print(f"Сумма: {amount} {currency}")


def main():
    """
    Функция получения и вывода полученных транзакций согласно введённым параметрам пользователя.

    Returns: Формат файла для открытия базы транзакций
    """
    # Главные герои
    user = "Пользователь"
    program = "Программа"

    # Получение файлов настроек для отобрежения файлов
    parameters = get_parameters(user, program)

    # Расскоментировать для быстрого тестирования различных наборов параметров
    # parameters = {'file_type': 'XLSX',
    #               'filter_status': 'EXECUTED',
    #               'sort_by_date': True,
    #               'sort': False,
    #               'show_rub_transactions': True,
    #               'filter_word': 'организ'}

    # 1. Чтение файла
    if parameters["file_type"] == "JSON":
        transactions = read_json("../data/operations.json")

    if parameters["file_type"] == "CSV":
        transactions = read_file_from_csv("../data/transactions.csv")

    if parameters["file_type"] == "XLSX":
        transactions = read_file_from_xlsx("../data/transactions_excel.xlsx")

    # 2. Получение словарей согласно настройке state
    filtered_transactions = filter_by_state(transactions, state_key=parameters["filter_status"])

    # 3. олучение словарей отсортированных по дате
    if parameters["sort_by_date"]:
        filtered_transactions = sort_by_date(filtered_transactions, sort_way=parameters["sort"])

    # 4. Получение рублёвых операций
    if parameters["show_rub_transactions"]:
        filtered_transactions = list(filter_by_currency(filtered_transactions, currency="RUB"))

    # 5. Получение отфильтрованных транзакицй по слову в описании
    if "filter_word" in parameters:
        filtered_transactions = process_bank_search(filtered_transactions, parameters["filter_word"])

    if not filtered_transactions:
        print(f"\n{program}: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\n{program}: Распечатываю итоговый список транзакций...")
        print(f"\n{program}:\nВсего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        print_transaction_info(transaction)
