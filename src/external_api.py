import json

import requests

from src.utils import read_json
import os
from dotenv import load_dotenv

operations = read_json('../data/operations.json')


def convert_transactions_to_rub(transaction: dict):
    load_dotenv()
    API_LAYER_KEY = os.getenv('API_LAYER_KEY')

    try:
        from_currency = transaction.get('operationAmount').get('currency').get('code')
        to_currency = 'RUB'
        amount = transaction.get('operationAmount').get('amount')

        if from_currency == to_currency:
            return amount
        else:

            payload = {}
            headers = {
                "apikey": API_LAYER_KEY
            }

            url = f'https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}'
            response = requests.request("GET", url, headers=headers, data=payload)

            parsed_result = json.loads(response.text)
            parsed_amount = parsed_result.get('result')

        return parsed_amount

    except Exception as e:
        raise ValueError(f"В транзакции отсутствует поле: {e}. Данные: {transaction}") from e


result = convert_transactions_to_rub(operations[0])
print(f'{result} рублей')
