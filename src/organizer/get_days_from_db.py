import sqlite3
from src.organizer.links import path_to_db


def get_days_from_db(date: str, version: str = 'last') -> tuple:
    """
    Позволяет получить кортеж c записью из БД days по
    дате и версии.

    date (str) - дата по которой получить расписание в формате
    'dd.mm.yy'.
    version (str) - версия расписания на день - натуральные числа от 0.
    Применимо для получения прошлых версий расписаний для аналитики,
    возврата к старым шаблонам и пр. Также поддерживает формат 'last' -
    для получения последней версии расписания. И 'first' для первой.

    rows(list) - список с кортежем, содержит нужную нам запись из БД days.
    """

    # Создаем соединение с базой данных
    with sqlite3.connect(path_to_db) as conn:
        # Создаем курсор
        cursor = conn.cursor()
        # Формируем SQL-запрос
        if version == 'last':
            sql_query = ("SELECT * FROM days WHERE date = ? ORDER BY version "
                         "DESC LIMIT 1")
            cursor.execute(sql_query, (date,))
        elif version == 'first':
            sql_query = ("SELECT * FROM days WHERE date = ? ORDER BY version "
                         "ASC LIMIT 1")
            cursor.execute(sql_query, (date,))
        else:
            sql_query = "SELECT * FROM days WHERE date = ? AND version = ?"
            cursor.execute(sql_query, (date, int(version)))
        # Получаем результаты
        rows = cursor.fetchall()
        if len(rows) == 0:
            return ()
        else:
            return rows[0]


if __name__ == '__main__':
    a = get_days_from_db('28.06.24')
    print(a)
