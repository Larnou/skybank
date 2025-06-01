import datetime


from time import time

def write_log_to_file(filename: str, data_log: list):
    with open(filename, "w", encoding="utf-8") as f:
        for line in data_log:
            f.write(line + '\n')

def log(filename: str = None):
    def func_decorator(func):
        # @wraps(func)
        def wrapper(*args, **kwargs):
            # Описание времени вызова
            time_in_seconds = time()
            date = datetime.datetime.fromtimestamp(time_in_seconds)
            date_formatted = date.strftime("%d.%m.%Y %H:%M:%S")
            date_log = f'Time to access the function: {date_formatted}'

            log_data = [date_log]
            name_log = f'Function name: {func.__name__}()'
            log_data.append(name_log)
            args_log = f'Arguments used: {args} и {kwargs}'

            try:
                result = func(*args, **kwargs)
                result_log = f'The result of the function execution {func.__name__}(): {result}\n'
                log_data.append(result_log)

                if filename:
                    write_log_to_file(filename, log_data)
                else:
                    print(*log_data, sep='\n')

                return result
            except Exception as e:
                error_log = f'\n{e}\n{args_log}'
                log_data.append(error_log)

                if filename:
                    write_log_to_file(filename, log_data)
                else:
                    print(*log_data, sep='\n')
                return None

        return wrapper
    return func_decorator
