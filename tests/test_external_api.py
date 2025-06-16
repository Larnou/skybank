from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_transactions_to_rub


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_same_currency_rub(mock_dotenv, mock_getenv, mock_request, example_of_rub_transactions):
    """Тест когда валюта уже в RUB"""
    result = convert_transactions_to_rub(example_of_rub_transactions)
    assert result == "1000"
    mock_dotenv.assert_called_once()
    mock_request.assert_not_called()


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_convert_currency_success(mock_dotenv, mock_getenv, mock_request, example_of_usd_transactions):
    """Тест успешной конвертации валюты"""
    # Настраиваем моки
    mock_getenv.return_value = "test_api_key"

    # Мок ответа API
    mock_response = MagicMock()
    mock_response.text = '{"result": 7977.9066}'
    mock_request.return_value = mock_response

    result = convert_transactions_to_rub(example_of_usd_transactions)
    assert result == 7977.9066

    # Проверяем вызов API
    mock_request.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100",
        headers={"apikey": "test_api_key"},
        data={},
    )


@patch("src.external_api.requests.request")
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_invalid_json_response(mock_dotenv, mock_getenv, mock_request, example_of_usd_transactions):
    """Тест невалидного JSON в ответе API"""
    mock_getenv.return_value = "test_api_key"

    # Мок ответа с битым JSON
    mock_response = MagicMock()
    mock_response.text = "INVALID_JSON"
    mock_request.return_value = mock_response

    with pytest.raises(ValueError) as excinfo:
        convert_transactions_to_rub(example_of_usd_transactions)

    assert "В транзакции отсутствует поле" in str(excinfo.value)
    assert "Данные:" in str(excinfo.value)
