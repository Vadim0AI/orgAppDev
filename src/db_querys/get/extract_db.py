import sqlite3


def extract_db(select_column: str, path_db: str, table_name: str, order_by: str = None) -> list[tuple]:
    """ Извлекает из БД список с содержимым.
    path_db (str) - путь к базе данных;
    table_name (str) - имя таблицы БД;
    order_by (str) - имя столбца для сортировки (опционально).
    """

    # Подключаемся к базе данных SQLite
    with sqlite3.connect(path_db) as conn:
        # Создаем объект курсора
        cursor = conn.cursor()

        # Формируем SQL-запрос с учетом возможной сортировки
        if order_by:
            query = f'SELECT {select_column} FROM {table_name} ORDER BY {order_by}'
        else:
            query = f'SELECT {select_column} FROM {table_name}'

        # Используем курсор для выполнения запроса
        cursor.execute(query)
        result = cursor.fetchall()
        return result