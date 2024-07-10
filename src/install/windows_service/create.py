import win32serviceutil
import win32service
import win32event
import win32api
import win32process
import win32con  # Добавим импорт win32con
import psutil

import subprocess
import time


class PythonScriptService(win32serviceutil.ServiceFramework):
    _svc_name_ = "orgApp"
    _svc_display_name_ = "orgApp"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)


    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


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


    def SvcDoRun(self):
        script_name = r'C:\Code\orgApp Dev\tests\two_window_scr\scr1.py'
        bat_file_path = r'C:\Code\orgApp Dev\tests\two_window_scr\run_scr2.bat'
        while True:
            # Проверяем, запущен ли процесс с определенным именем
            if not self.is_script_running(script_name):
                # Если процесс не запущен, запускаем скрипт Python
                subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)

            # Период ожидания перед повторной проверкой (в секундах)
            time.sleep(10)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PythonScriptService)
