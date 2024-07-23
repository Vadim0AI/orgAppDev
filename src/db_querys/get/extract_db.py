import sqlite3

def extract_db(select_column: str, path_db: str, table_name: str, where_condition: str = None, order_by: str = None) -> list[tuple]:
    """ Извлекает из БД список с содержимым.
    select_column (str) - какие столбцы берем, если все, то нужно *;
    path_db (str) - путь к базе данных;
    table_name (str) - имя таблицы БД;
    where_condition (str) - условие WHERE для фильтрации данных (опционально);
    order_by (str) - имя столбца для сортировки (опционально).
    """

    # Подключаемся к базе данных SQLite
    with sqlite3.connect(path_db) as conn:
        # Создаем объект курсора
        cursor = conn.cursor()

        # Формируем SQL-запрос с учетом возможных условий WHERE и сортировки
        query = f'SELECT {select_column} FROM {table_name}'
        if where_condition:
            query += f' WHERE {where_condition}'
        if order_by:
            query += f' ORDER BY {order_by}'

        # Используем курсор для выполнения запроса
        cursor.execute(query)
        result = cursor.fetchall()
        return result