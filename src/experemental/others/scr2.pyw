import os
import time
import psutil
from path_global import path_scr1, path_py_interpreter, t_sleep
import subprocess
from write_log import write_log
import signal
import sys


def is_script_running(script_name):
    """
    Проверяет, запущен ли скрипт Python с заданным именем.

    Args:
    script_name (str): Имя скрипта Python для проверки.

    Returns:
    bool: True, если скрипт запущен, и False в противном случае.
    """
    # Получаем список всех запущенных процессов
    for proc in psutil.process_iter(['pid', 'name']):
        # Проверяем, что имя процесса совпадает с именем скрипта
        if proc.info['name'] == 'python.exe':
            # Получаем список аргументов командной строки процесса
            cmdline = proc.cmdline()
            # Проверяем, что имя запущенного скрипта присутствует в аргументах командной строки
            if len(cmdline) >= 2 and cmdline[1] == script_name:
                return True
    return False

print("Скрипт 2 запущен")

while True:
    # Пример использования функции
    if is_script_running(path_scr1):
        # print("Скрипт 2: Скрипт 1 запущен")
        write_log("Скрипт 2: Скрипт 1 запущен")
        t_sleep = 1
    else:
        write_log("Скрипт 2: Скрипт 1 НЕ запущен")
        # print("Скрипт 2: Скрипт 1 НЕ запущен")
        # Запускаем скрипт 1
        process = subprocess.Popen([path_py_interpreter, path_scr1],
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        # os.system('shutdown /s /t 10')
        t_sleep = 0

    time.sleep(t_sleep)

# TODO: Добавить функционал защиты от неполного выключения, когда при
#  завершении одного скрипта через выключение ПК, второй выключает
#  принудительно ПК и наоборот