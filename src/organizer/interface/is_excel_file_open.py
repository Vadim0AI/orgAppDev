import psutil

import psutil


def is_excel_file_open(file_path):
    """
    Проверяет, открыт ли файл Excel с помощью WPS Office.

    Args:
        file_path (str): Путь к файлу Excel.

    Returns:
        bool: True, если файл открыт, False в противном случае.
    """
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path and 'wps.exe' in exe_path:
                cmdline = proc.cmdline()
                if any(file_path in arg for arg in cmdline):
                    return True
        except (
        psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if __name__ == '__main__':
    # Пример использования
    excel_file_path = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'
    if is_excel_file_open(excel_file_path):
        print(f"Файл {excel_file_path} открыт с помощью WPS Office.")
    else:
        print(f"Файл {excel_file_path} не открыт с помощью WPS Office.")