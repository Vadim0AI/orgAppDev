import os
import time
import psutil
from path_global import path_scr2, path_py_interpreter, t_sleep
import subprocess
from write_log import write_log






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

# f = open(r"C:\Code\orgApp Dev\src\run\not_close_windows.txt", 'w')
# f.write('text')

process = subprocess.Popen([path_py_interpreter, path_scr2], creationflags=subprocess.CREATE_NO_WINDOW)
time.sleep(2)

# TODO: Запустить проверку запуска проверяющего защитного скрипта scr2.py в
#  отельном потоке

while True:
    # Пример использования функции
    if is_script_running(path_scr2):
        write_log("Скрипт 1: Скрипт 2 запущен")
        # print("Скрипт 1: Скрипт 2 запущен")
        t_sleep = 1
    else:
        write_log("Скрипт 1: Скрипт 2 НЕ запущен")
        # print("Скрипт 1: Скрипт 2 НЕ запущен")
        # Запускаем скрипт 2
        process = subprocess.Popen([path_py_interpreter, path_scr2],
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        # os.system('shutdown /s /t 10')
        t_sleep = 0

    time.sleep(t_sleep)
