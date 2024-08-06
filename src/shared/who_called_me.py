import inspect

def who_called_me():
    # Получаем текущий стек вызовов
    stack = inspect.stack()
    # Второй элемент стека (индекс 1) содержит информацию о вызывающей функции
    caller_frame = stack[2]
    # Получаем имя вызывающей функции
    caller_name = caller_frame.function
    print(f"Функция была вызвана из: {caller_name}")
