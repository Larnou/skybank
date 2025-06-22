from unittest.mock import patch

from src.main_utils import welcome_user, get_filter_status, get_parameters


def test_welcome_user_valid_input_json(capsys):
    """Тест валидного выбора JSON формата"""
    user_inputs = ["1"]
    expected_output = "JSON"

    with patch('builtins.input', side_effect=user_inputs):
        result = welcome_user("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == expected_output
    assert "Для обработки выбран JSON-файл." in captured.out


def test_welcome_user_valid_input_csv(capsys):
    """Тест валидного выбора CSV формата"""
    user_inputs = ["2"]
    expected_output = "CSV"

    with patch('builtins.input', side_effect=user_inputs):
        result = welcome_user("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == expected_output
    assert "Для обработки выбран CSV-файл." in captured.out


def test_welcome_user_valid_input_xlsx(capsys):
    """Тест валидного выбора XLSX формата"""
    user_inputs = ["3"]
    expected_output = "XLSX"

    with patch('builtins.input', side_effect=user_inputs):
        result = welcome_user("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == expected_output
    assert "Для обработки выбран XLSX-файл." in captured.out


def test_welcome_user_output_structure(capsys):
    """Тест структуры выводимого сообщения"""
    user_inputs = ["1"]

    with patch('builtins.input', side_effect=user_inputs):
        welcome_user("TestUser", "TestProgram")

    captured = capsys.readouterr()
    output = captured.out

    assert "TestProgram: Привет! Добро пожаловать в программу работы с банковскими транзакциями." in output
    assert "Добро пожаловать в программу работы с банковскими транзакциями." in output
    assert "Выберите необходимый пункт меню:" in output
    assert "1. Получить информацию о транзакциях из JSON-файла" in output
    assert "2. Получить информацию о транзакциях из CSV-файла" in output
    assert "3. Получить информацию о транзакциях из XLSX-файла" in output
    assert "Для обработки выбран JSON-файл." in output


def test_welcome_user_invalid_input_then_valid(capsys):
    """Тест невалидного ввода с последующим валидным"""
    user_inputs = ["5", "2"]  # Сначала неверный, потом верный ввод
    expected_output = "CSV"

    with patch('builtins.input', side_effect=user_inputs):
        result = welcome_user("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == expected_output
    # Проверяем что обработка продолжилась после ошибки
    assert "Для обработки выбран CSV-файл." in captured.out


def test_valid_status_executed(capsys):
    """Тест корректного ввода статуса EXECUTED"""
    user_inputs = ["EXECUTED"]

    with patch('builtins.input', side_effect=user_inputs):
        result = get_filter_status("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == "EXECUTED"
    assert 'Введите статус, по которому необходимо выполнить фильтрацию.' in captured.out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured.out


def test_valid_status_canceled(capsys):
    """Тест корректного ввода статуса CANCELED"""
    user_inputs = ["CANCELED"]

    with patch('builtins.input', side_effect=user_inputs):
        result = get_filter_status("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == "CANCELED"
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured.out


def test_valid_status_pending(capsys):
    """Тест корректного ввода статуса PENDING"""
    user_inputs = ["PENDING"]

    with patch('builtins.input', side_effect=user_inputs):
        result = get_filter_status("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == "PENDING"
    assert 'Операции отфильтрованы по статусу "PENDING"' in captured.out


def test_case_insensitivity(capsys):
    """Тест нечувствительности к регистру ввода"""
    user_inputs = ["PeNdInG"]

    with patch('builtins.input', side_effect=user_inputs):
        result = get_filter_status("TestUser", "TestProgram")

    captured = capsys.readouterr()
    assert result == "PENDING"
    assert 'Операции отфильтрованы по статусу "PENDING"' in captured.out


def test_invalid_then_valid_status(capsys):
    """Тест неверного ввода с последующим корректным"""
    user_inputs = ["WRONG_STATUS", "EXECUTED"]

    with patch('builtins.input', side_effect=user_inputs):
        result = get_filter_status("TestUser", "TestProgram")

    captured = capsys.readouterr()
    output = captured.out

    assert result == "EXECUTED"
    # Проверяем сообщение об ошибке
    assert 'Статус операции "WRONG_STATUS" недоступен.' in output
    # Проверяем повторный вывод меню
    assert output.count('Введите статус, по которому необходимо выполнить фильтрацию.') == 2
    assert output.count('Доступные для фильтровки статусы:') == 2


# Тест минимальных параметров (все ответы "нет")
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="JSON")
@patch('src.main_utils.get_filter_status', return_value="EXECUTED")
@patch('builtins.input')
def test_minimal_parameters(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест с минимальным набором параметров"""
    mock_input.side_effect = [
        "нет",  # Сортировать по дате?
        "нет",  # Только рублевые?
        "нет"  # Фильтр по описанию?
    ]

    params = get_parameters("User", "Program")

    assert params == {
        "file_type": "JSON",
        "filter_status": "EXECUTED",
        "show_rub_transactions": False
    }
    # Проверяем отсутствие необязательных параметров
    assert "sort_by_date" not in params
    assert "sort" not in params
    assert "filter_word" not in params


# Тест с полным набором параметров
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="CSV")
@patch('src.main_utils.get_filter_status', return_value="PENDING")
@patch('builtins.input')
def test_full_parameters(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест со всеми возможными параметрами"""
    mock_input.side_effect = [
        "да",  # Сортировать по дате?
        "по возрастанию",  # Направление сортировки
        "да",  # Только рублевые?
        "да",  # Фильтр по описанию?
        "перевод"  # Слово для фильтра
    ]

    params = get_parameters("User", "Program")

    assert params == {
        "file_type": "CSV",
        "filter_status": "PENDING",
        "sort_by_date": True,
        "sort": True,
        "show_rub_transactions": True,
        "filter_word": "перевод"
    }


# Тест сортировки по возрастанию
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="XLSX")
@patch('src.main_utils.get_filter_status', return_value="CANCELED")
@patch('builtins.input')
def test_ascending_sort(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест сортировки по возрастанию"""
    mock_input.side_effect = [
        "да",  # Сортировать по дате?
        "возрастание",  # Направление сортировки
        "нет",  # Только рублевые?
        "нет"  # Фильтр по описанию?
    ]

    params = get_parameters("User", "Program")
    assert params["sort_by_date"] is True
    assert params["sort"] is True


# Тест сортировки по убыванию
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="JSON")
@patch('src.main_utils.get_filter_status', return_value="EXECUTED")
@patch('builtins.input')
def test_descending_sort(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест сортировки по убыванию"""
    mock_input.side_effect = [
        "да",  # Сортировать по дате?
        "убыванию",  # Направление сортировки
        "нет",  # Только рублевые?
        "нет"  # Фильтр по описанию?
    ]

    params = get_parameters("User", "Program")
    assert params["sort_by_date"] is True
    assert params["sort"] is False


# Тест без сортировки по дате
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="CSV")
@patch('src.main_utils.get_filter_status', return_value="PENDING")
@patch('builtins.input')
def test_no_date_sorting(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест без сортировки по дате"""
    mock_input.side_effect = [
        "нет",  # Сортировать по дате?
        "да",  # Только рублевые?
        "нет"  # Фильтр по описанию?
    ]

    params = get_parameters("User", "Program")
    assert "sort_by_date" not in params
    assert "sort" not in params
    assert params["show_rub_transactions"] is True


# Тест фильтрации по описанию
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="JSON")
@patch('src.main_utils.get_filter_status', return_value="EXECUTED")
@patch('builtins.input')
def test_description_filter(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест фильтра по описанию транзакции"""
    mock_input.side_effect = [
        "нет",  # Сортировать по дате?
        "нет",  # Только рублевые?
        "да",  # Фильтр по описанию?
        "покупка"  # Слово для фильтра
    ]

    params = get_parameters("User", "Program")
    assert params["filter_word"] == "покупка"


# Тест без фильтрации по описанию
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="CSV")
@patch('src.main_utils.get_filter_status', return_value="CANCELED")
@patch('builtins.input')
def test_no_description_filter(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест без фильтра по описанию"""
    mock_input.side_effect = [
        "нет",  # Сортировать по дате?
        "нет",  # Только рублевые?
        "нет"  # Фильтр по описанию?
    ]

    params = get_parameters("User", "Program")
    assert "filter_word" not in params


# Тест с различными вариантами ответов для сортировки
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="JSON")
@patch('src.main_utils.get_filter_status', return_value="EXECUTED")
@patch('builtins.input')
def test_sort_variants(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест различных вариантов ответа для сортировки"""
    variants = [
        "возрастанию",
        "возрастание",
        "по возрастанию",
        "убыванию",
        "убывание",
        "по убыванию"
    ]

    for variant in variants:
        mock_input.side_effect = [
            "да",  # Сортировать по дате?
            variant,  # Направление сортировки
            "нет",  # Только рублевые?
            "нет"  # Фильтр по описанию?
        ]

        params = get_parameters("User", "Program")
        assert params["sort_by_date"] is True

        if "возраста" in variant:
            assert params["sort"] is True
        else:
            assert params["sort"] is False


# Тест с нечувствительностью к регистру
@patch('builtins.print')
@patch('src.main_utils.welcome_user', return_value="XLSX")
@patch('src.main_utils.get_filter_status', return_value="PENDING")
@patch('builtins.input')
def test_case_insensitivity(mock_input, mock_get_filter_status, mock_welcome_user, mock_print):
    """Тест нечувствительности к регистру"""
    mock_input.side_effect = [
        "Да",
        "ВОЗРАСТАНИЮ",
        "дА",
        "Да",
        "ПокупКА"
    ]

    params = get_parameters("User", "Program")
    assert params["sort_by_date"] is True
    assert params["sort"] is True
    assert params["show_rub_transactions"] is True
    assert params["filter_word"] == "покупка"