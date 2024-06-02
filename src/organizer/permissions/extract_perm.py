import sqlite3


def extract_perm(db: str, wb_title: str, type_perm: str):
    """ Извлекает разрешения для close ли blocked и помещает их в
    соответствующие списки

    type_perm - 'close' or 'blocked'

    """
    # Извлекаем список close из базы данных
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect(db)
    # Создаем объект курсора
    cursor = conn.cursor()
    # Выполняем SQL-запрос для выборки данных
    cursor.execute(f'SELECT {type_perm} FROM wb WHERE title = ?',
                   (wb_title,))
    # Получаем список разрешений для close или blocked
    close_str = cursor.fetchall()[0][0]

    # Получаем два отдельных списка process_names и dir_names
    close_list = close_str.split(sep=' | ')
    process_names: str = close_list[0]
    dir_names: str = ''
    if len(close_list) > 1:
        dir_names = close_list[1]
    process_names: list = process_names.split(sep=', ')
    dir_names: list = dir_names.split(sep=', ')
    return process_names, dir_names
