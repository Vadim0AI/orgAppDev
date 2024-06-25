import sqlite3


def get_days_from_db(date: str, version: str = 'last'):
    """
    Позволяет получить строку расписания на день из БД days по
    дате и версии.

    date (str) - дата по которой получить расписание в формате
    'dd.mm.yy'.
    version (str) - версия расписания не день в формате (пример) '1.2.1'.
    Применимо для получения прошлых версий расписаний для аналитики,
    возврата к старым шаблонам и пр. Также поддерживает формат 'last' -
    для получения последней версии расписания. И 'first' для первой.

    rows - возвращает строку из БД days. Это список кортежей (если строк
    несколько), но поскольку при любом запросе должна выводится одна строка,
    то должен быть tuple.
    """

    # Создаем соединение с базой данных
    with sqlite3.connect('test.db') as conn:
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
            cursor.execute(sql_query, (date, version))
        # Получаем результаты
        rows = cursor.fetchall()
        return rows
