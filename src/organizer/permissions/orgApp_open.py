import os
import subprocess
import webbrowser
import sqlite3


def open_file_app_dir_url(wb_title: str, db: str, program="explorer",
                          chrome_path=r"C:/Program Files/Google/Chrome/Application/chrome.exe %s"):
    """ Открывает директорию в файловом менеджере или URL в браузере """

    # Извлекаем список close из базы данных
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect(db)
    # Создаем объект курсора
    cursor = conn.cursor()
    # Выполняем SQL-запрос для выборки данных
    cursor.execute(f'SELECT open FROM wb WHERE title = ?',
                   (wb_title,))
    # Получаем строку для open
    path_or_url: str = cursor.fetchall()[0][0]
    # Преобразуем в список
    path_or_url: list = path_or_url.split(sep=', ')

    # Выполняем открытие файлов или URL
    for pu in path_or_url:
        if os.path.exists(pu):
            subprocess.run([program, pu])
        else:
            webbrowser.get(chrome_path).open(pu)
