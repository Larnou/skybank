from src.decorators import log

# Используйте pytest для написания тестов, проверяющих функциональность декоратора.
# Для тестирования вывода в консоль примените фикстуру capsys, которая позволяет перехватывать вывод данных в консоль.
# Убедитесь, что тесты покрывают различные сценарии использования декоратора,
# включая успешное выполнение функций и обработку исключений.


def successful_function(a, b):
    return a + b


def failing_function():
    raise ValueError("Test error")


def test_log_success_console(capsys):
    @log()
    def test_func(x, y):
        return x * y

    result = test_func(3, 4)
    captured = capsys.readouterr()
    output = captured.out

    assert result == 12
    assert "Function name: test_func()" in output
    assert "The result of the function execution test_func(): 12" in output


def test_log_success_file(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def test_func(a, b, c=10):
        return a + b + c

    result = test_func(5, 7, c=3)
    content = log_file.read_text()

    assert result == 15
    assert "Function name: test_func()" in content
    assert "The result of the function execution test_func(): 15" in content


def test_log_exception_console(capsys):
    @log()
    def test_func():
        failing_function()

    result = test_func()
    captured = capsys.readouterr()
    output = captured.out

    assert result is None
    assert "Function name: test_func()" in output
    assert "Test error" in output
    assert "Arguments used: () and {}" in output


def test_log_exception_file(tmp_path):
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def test_division_func(a, b=0):
        return a / b

    result = test_division_func(10, 0)
    content = log_file.read_text()

    assert result is None
    assert "Function name: test_division_func()" in content
    assert "division by zero" in content
    assert "Arguments used: (10, 0) and {}" in content
