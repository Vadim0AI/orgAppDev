import os
import subprocess
import webbrowser


def open_file_app_dir_url(path_or_url, program="explorer",
                          chrome_path=r"C:/Program Files/Google/Chrome/Application/chrome.exe %s"):
    """Открывает директорию в файловом менеджере или URL в браузере"""
    if os.path.exists(path_or_url):
        subprocess.run([program, path_or_url])
    else:
        webbrowser.get(chrome_path).open(path_or_url)