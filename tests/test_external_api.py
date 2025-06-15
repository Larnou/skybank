import pytest

from src.external_api import convert_transactions_to_rub
from unittest.mock import Mock, MagicMock
from unittest.mock import patch
import requests


@patch('src.external_api.requests.request')
@patch('src.external_api.os.getenv')
@patch('src.external_api.load_dotenv')
def test_same_currency_rub(mock_dotenv, mock_getenv, mock_request):
    """Тест когда валюта уже в RUB"""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {'code': 'RUB'}
        }
    }

    result = convert_transactions_to_rub(transaction)
    assert result == '100.0'
    mock_dotenv.assert_called_once()
    mock_request.assert_not_called()


@patch('src.external_api.requests.request')
@patch('src.external_api.os.getenv')
@patch('src.external_api.load_dotenv')
def test_convert_currency_success(mock_dotenv, mock_getenv, mock_request):
    """Тест успешной конвертации валюты"""
    # Настраиваем моки
    mock_getenv.return_value = 'test_api_key'

    # Мок ответа API
    mock_response = MagicMock()
    mock_response.text = '{"result": 7500.50}'
    mock_request.return_value = mock_response

    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {'code': 'USD'}
        }
    }

    result = convert_transactions_to_rub(transaction)
    assert result == 7500.50

    # Проверяем вызов API
    mock_request.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0",
        headers={"apikey": "test_api_key"},
        data={}
    )


@patch('src.external_api.requests.request')
@patch('src.external_api.os.getenv')
@patch('src.external_api.load_dotenv')
def test_invalid_json_response(mock_dotenv, mock_getenv, mock_request):
    """Тест невалидного JSON в ответе API"""
    mock_getenv.return_value = 'test_api_key'

    # Мок ответа с битым JSON
    mock_response = MagicMock()
    mock_response.text = 'INVALID_JSON'
    mock_request.return_value = mock_response

    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {'code': 'JPY'}
        }
    }

    with pytest.raises(ValueError) as excinfo:
        convert_transactions_to_rub(transaction)

    assert "В транзакции отсутствует поле" in str(excinfo.value)
    assert "Данные:" in str(excinfo.value)