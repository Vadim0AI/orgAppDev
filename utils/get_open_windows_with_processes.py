import win32gui
import win32process
import psutil

# Получить название всех открытых окон, соответствующие им процессы и дескрипторы окон

def get_open_windows_with_processes():
    """
        Перечисляет все видимые окна в системе и собирает информацию о каждом окне, включая его дескриптор (hwnd), заголовок окна,
        имя процесса и PID процесса. Эта информация возвращается в виде списка кортежей.

        Функция использует API Windows для перечисления окон и получения информации о процессе, который создал каждое окно.

        Внутренняя функция enum_windows_callback вызывается для каждого окна, найденного функцией win32gui.EnumWindows.

        - hwnd: Дескриптор окна.
        - results: Список результатов, который будет заполнен кортежами, содержащими информацию об окнах.

        Для каждого видимого окна проверяется, имеет ли оно заголовок (window_text).
        Если заголовок существует, функция получает PID процесса, связанного с окном, и имя процесса,
        используя win32process и psutil. Эти данные добавляются в список результатов.

        Возвращаемое значение:
            Список кортежей, где каждый кортеж содержит:
            - hwnd (int): Дескриптор окна.
            - window_text (str): Заголовок окна.
            - process_name (str): Имя процесса.
            - pid (int): PID процесса.

        Пример использования:
            windows = get_open_windows_with_processes()
            for hwnd, window_text, process_name, pid in windows:
                print(f"HWND: {hwnd}, Window: {window_text}, Process: {process_name}, PID: {pid}")
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

def main():
    windows = get_open_windows_with_processes()
    for hwnd, window_text, process_name, pid in windows:
        print(f"HWND: {hwnd}, Window: {window_text}, Process: {process_name}, PID: {pid}")

if __name__ == '__main__':
    main()
