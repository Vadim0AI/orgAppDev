import psutil


def is_script_running(self, script_name):
    """
    Проверяет, запущен ли скрипт Python с заданным именем.

    Args:
    script_name (str): Имя скрипта Python для проверки.

    Returns:
    bool: True, если скрипт запущен, и False в противном случае.
    """
    script_name = r'C:\Code\orgApp Dev\tests\two_window_scr\scr1.py'
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