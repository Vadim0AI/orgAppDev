import ctypes
import sys

def run_as_admin(command, params=None, folder=None):
    try:
        if sys.platform.lower().startswith("win"):
            shell32 = ctypes.windll.shell32
            if folder:
                folder = str(folder)
            ret = shell32.ShellExecuteW(None, "runas", command, params, folder, 1)
            if ret <= 32:
                raise ctypes.WinError(ret)
        else:
            raise RuntimeError("This function is only implemented on Windows.")
    except Exception as e:
        print(f"Error: {e}")

# Замените "python" на путь к вашему интерпретатору Python
command = r"C:\Code\orgApp Dev\venv\Scripts\python.exe"
script_path = r"C:\Code\orgApp Dev\src\organizer\permissions\orgApp_close.py"
params = None  # Можно передать аргументы скрипту, если нужно

run_as_admin(command, script_path, params)