from datetime import datetime

import pandas as pd

from src.utils import read_json
from src.parser import read_file_from_csv, read_file_from_xlsx
from src.processing import filter_by_state, sort_by_date

def welcome_user(user, program):
    print(f'{program}: Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')

    menu_variants = {
        1: '1. Получить информацию о транзакциях из JSON-файла',
        2: '2. Получить информацию о транзакциях из CSV-файла',
        3: '3. Получить информацию о транзакциях из XLSX-файла'
    }

    for i in range(1, len(menu_variants) + 1):
        print(menu_variants.get(i))

    user_choice = int(input(f'\n{user}: '))
    program_answer = menu_variants.get(user_choice).split(' ')[-1][:-1]
    print(f'\n{program}: Для обработки выбран {program_answer}.')

    file_type = program_answer.split('-')[0]
    return file_type



def get_filter_status(user, program):
    status_variants = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print(f'\n{program}: Введите статус, по которому необходимо выполнить фильтрацию.')
        print(f'Доступные для фильтровки статусы: {', '.join(status_variants)}\n')

        user_choice = input(f'{user}: ').upper()
        if user_choice in status_variants:
            print(f'{program}: Операции отфильтрованы по статусу "{user_choice}"')
            return user_choice
        else:
            print(f'\n{program}: Статус операции "{user_choice}" недоступен.')



def get_parameters(user, program):
    file_type = welcome_user(user, program)
    filter_status = get_filter_status(user, program)

    # Дополнительные вопросы

    print(f'\n{program}: Отсортировать операции по дате? Да/Нет\n')
    user_choice_datasort = input(f'{user}: ').lower()
    sort_by_date = True if user_choice_datasort == 'да' else False

    print(f'\n{program}: Отсортировать по возрастанию или по убыванию?\n')
    user_choice_sort = input(f'{user}: ').lower()
    sort = True if user_choice_sort in ['возрастанию', 'возрастание', 'по возрастанию'] else False

    print(f'\n{program}: Выводить только рублевые транзакции? Да/Нет\n')
    user_choice_rub = input(f'{user}: ').lower()
    show_rub_transactions = True if user_choice_rub == 'да' else False

    # На данном этапе получены все обязательные ответы, которые содержат ответ.
    parameters = {
        'file_type': file_type,
        'filter_status': filter_status,
        'sort_by_date': sort_by_date,
        'sort': sort,
        'show_rub_transactions': show_rub_transactions
    }

    print(f'\n{program}: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n')
    user_choice_filter_description = input(f'{user}: ').lower()
    if user_choice_filter_description == 'да':
        print(f'\n{program}: Введите необходимое слово в описании транзакции.\n')
        filter_word = input(f'{user}: ').lower()
        parameters['filter_word'] = filter_word


    return parameters

def show_filtered_transactions():
    # Главные герои
    user = 'Пользователь'
    program = 'Программа'

    # Получение файлов настроек для отобрежения файлов
    parameters = get_parameters(user, program)

    # 1. Чтение файла
    if parameters['file_type'] == 'JSON':
        transactions = read_json('../data/operations.json')

    if parameters['file_type'] == 'CSV':
        transactions = read_file_from_csv('../data/transactions.csv')

    if parameters['file_type'] == 'XLSX':
        transactions = read_file_from_xlsx('../data/transactions_excel.xlsx')


    # 2. Получение словарей согласно настройке state
    filtered_by_state = filter_by_state(transactions, state_key=parameters['filter_status'])

    # 3. олучение словарей отсортированных по дате
    # sorted_by_date = sort_by_date(filtered_by_state, sort_way=parameters['sort_by_date'])



    filtered_transactions = [1,2,3,4,5,6,7]
    print(f'\n{program}: Распечатываю итоговый список транзакций...')
    print(f'\n{program}:\nВсего банковских операций в выборке: {len(filtered_by_state)}')


    for i in range(5):
        print(filtered_by_state[i])




show_filtered_transactions()