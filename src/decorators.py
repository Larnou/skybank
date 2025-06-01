from typing import Callable, Any


def write_log_to_file(filename: str, data_log: list) -> None:
    """
    Записывает данные data_log в файл по пути filename.
    :param filename: Путь до файла, в котором будут записаны логи.
    :param data_log: Данные логирования работы.
    :return:
    """
    with open(filename, "w", encoding="utf-8") as f:
        for line in data_log:
            f.write(line + "\n")


def log(filename: str | None) -> Callable:
    """
    Декоратор, позволяющий проанализировать и отследить поведение функции.
    :param filename: Путь до файла, в котором будут записаны логи.
    :return:
    """
    def func_decorator(func) -> Any:
        # @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Описание времени вызова
            # time_in_seconds = time()
            # date = datetime.datetime.fromtimestamp(time_in_seconds)
            # date_formatted = date.strftime("%d.%m.%Y %H:%M:%S")
            # date_log = f'Time to access the function: {date_formatted}'

            log_data = []
            name_log = f"Function name: {func.__name__}()"
            log_data.append(name_log)
            args_log = f"Arguments used: {args} and {kwargs}"

            try:
                result = func(*args, **kwargs)
                result_log = f"The result of the function execution {func.__name__}(): {result}\n"
                log_data.append(result_log)

                if filename:
                    write_log_to_file(filename, log_data)
                else:
                    print(*log_data, sep="\n")

                return result
            except Exception as e:
                error_log = f"\n{e}\n{args_log}"
                log_data.append(error_log)

                if filename:
                    write_log_to_file(filename, log_data)
                else:
                    print(*log_data, sep="\n")
                return None

        return wrapper

    return func_decorator
