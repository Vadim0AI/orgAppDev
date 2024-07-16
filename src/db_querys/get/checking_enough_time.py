import sqlite3
from datetime import datetime
# TODO: Требуется протестировать


def checking_enough_time():
    """ Подключается к БД и проверяет по полю compiled_by, было ли
    вчера выделено достаточно времени для составления расписания на сегодня """
    # Подключение к базе данных
    conn = sqlite3.connect(r'/resources/db/orgApp.db')
    # Создание объекта курсора
    cur = conn.cursor()
    # Получение строки с сегодняшней датой в формате "dd_mm_yyyy_weekday"
    #   Получение сегодняшней даты
    today = datetime.today()
    #   Форматирование даты в строку с нужным форматом
    formatted_date = today.strftime('%d_%m_%Y_%a')
    # Выполнение SQL-запроса для выборки данных.
    #   Выбираем расписание на сегодня (оно должно быть одно в начале дня).
    cur.execute('''
        SELECT enough_time
        FROM days
        WHERE date = ?
        ''', (today,))
    # Получение результатов запроса
    enough_time = cur.fetchall()
    return enough_time