

from src.utils import read_json
import os
from dotenv import load_dotenv

operations = read_json('../data/operations.json')
# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной GITHUB_TOKEN из .env-файла
github_token = os.getenv('GITHUB_TOKEN')

def convert_transactions_tu_rub(transaction: dict) -> float:

    try:
         currency = transaction.get('operationAmount').get('currency').get('code')
    except Exception as e:
        raise ValueError(f"В транзакции отсутствует поле: {e}. Данные: {transaction}") from e

    return currency





result = convert_transactions_tu_rub(operations[1])
print(f'{result} рублей')
print(github_token)