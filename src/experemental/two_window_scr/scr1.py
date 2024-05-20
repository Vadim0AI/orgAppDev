import time
import psutil
import subprocess

# Путь к скрипту 2
path_scr2 = r'/tests/experemental/two_window_scr/scr2.py'

# Путь к вашему .bat файлу для запуска скрипта 2
bat_file_path = r'/tests/experemental/two_window_scr/run_scr2.bat'

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

try:
    while True:
        # Пример использования функции
        if is_script_running(path_scr2):
            print("Скрипт 1: Скрипт 2 запущен")
            time.sleep(3)
        else:
            print("Скрипт 1: Скрипт 2 НЕ запущен")
            # Запуск .bat файла
            subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
except BaseException as exc:
    subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)