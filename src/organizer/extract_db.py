import sqlite3


def extract_db(select_column: str, path_db: str, table_name: str) -> list:
    """ Извлекает из БД список с содержимым.
    path_db (str) - путь к базе данных;
    table_name (str) - имя листа БД;
    """

    # Подключаемся к базе данных SQLite
    with sqlite3.connect(path_db) as conn:
        # Создаем объект курсора
        cursor = conn.cursor()
        # Используем курсор для выполнения запросов
        cursor.execute(f'SELECT {select_column} FROM {table_name}')
        result = cursor.fetchall()
        return result
