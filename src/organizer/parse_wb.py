import sqlite3
from parse_table import parse_table



def parse_wb(db: str, path_wb: str):
    """ Парсит таблицу рабочих блоков (wb) с разрешениями и помещает в базу
    данных
    """

    table = tuple(parse_table(path_wb))

    # Помещаем значения списка в существующую базу данных SQLite
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        # Помещаем значения списка в таблицу
        for row in table:
            cursor.execute(
                '''INSERT INTO wb 
                (title, open, close, blocked) 
                VALUES (?, ?, ?, ?)''',
                row)
        # Сохраняем изменения
        conn.commit()