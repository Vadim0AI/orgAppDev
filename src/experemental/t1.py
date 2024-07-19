import win32gui
import win32process
import psutil
import os

def get_open_windows_with_processes():
    """
    Перечисляет все видимые окна в системе и собирает информацию о каждом окне, включая его дескриптор (hwnd), заголовок окна,
    имя процесса и PID процесса. Эта информация возвращается в виде списка кортежей.
    """
    def enum_windows_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text:  # Игнорируем окна без заголовка
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    results.append((hwnd, window_text, process.name(), pid))  # Добавляем hwnd в результаты
                except psutil.NoSuchProcess:
                    pass
        return True

    results = []
    win32gui.EnumWindows(enum_windows_callback, results)
    return results

def is_excel_file_open(file_path):
    """
    Проверяет, открыт ли файл Excel с помощью Microsoft Excel или WPS Office.
    """
    file_name = os.path.basename(file_path)
    windows = get_open_windows_with_processes()
    for hwnd, window_text, process_name, pid in windows:
        if ('EXCEL.EXE' in process_name.upper() or 'WPS.EXE' in process_name.upper()) and file_name in window_text:
            return True
    return False

def main():
    excel_file_path = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'
    if is_excel_file_open(excel_file_path):
        print(f"Файл {excel_file_path} открыт с помощью Microsoft Excel или WPS Office.")
    else:
        print(f"Файл {excel_file_path} не открыт с помощью Microsoft Excel или WPS Office.")

if __name__ == '__main__':
    main()