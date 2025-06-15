import json
import os

import requests
from dotenv import load_dotenv


def convert_transactions_to_rub(transaction: dict):
    """
    Возвращает конвертацию валюты в рублях, для конкретной транзакции.
    :param transaction: Транзакция, в которой необходимо произвести конвертацию валюты.
    :return: Значение в рублях, полученное после конвертации.
    """
    load_dotenv()
    API_LAYER_KEY = os.getenv("API_LAYER_KEY")

    try:
        from_currency = transaction.get("operationAmount").get("currency").get("code")
        to_currency = "RUB"
        amount = transaction.get("operationAmount").get("amount")

        if from_currency == to_currency:
            return amount
        else:

            payload = {}
            headers = {"apikey": API_LAYER_KEY}

            url_cite = "https://api.apilayer.com/exchangerates_data/convert"
            params = f"?to={to_currency}&from={from_currency}&amount={amount}"
            url = url_cite + params

            response = requests.request("GET", url, headers=headers, data=payload)

            parsed_result = json.loads(response.text)
            parsed_amount = parsed_result.get("result")

        return parsed_amount

    except Exception as e:
        raise ValueError(f"В транзакции отсутствует поле: {e}. Данные: {transaction}") from e
