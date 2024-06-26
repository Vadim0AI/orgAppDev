import sqlite3
from parse_table import parse_table

# TODO: Cейчас склоняюсь к тому, что эта функция не нужна, также как и
#  таблица базы данных "day_datailed" т.к. лучше сразу
#  спарсить подробное расписание на день, трансформировать его в расписание
#  по рабочим блокам, и затем уже в таком емком виде добавлять в базу
#  данных. По большей части такое расписание по 5 минут больше полезно как
#  интерфейс для редактирования и составления, но не для чтения и хранения.

# TODO: В будущем будет смысл в функции, которая извлекает расписание по
#  рабочим блокам из БД, преобразует его в детализированную форму по 5 минут
#  и помещает в таблицу excel в целях дальнейшего редактирования
#  пользователям, после автокорректирвоки / автосоставления расписания.


def parse_day(db: str, path_day: str, id_days: int):
    """ Парсит расписание Day_03_06_Mon.xlsx и помещает его в БД

    path_day (str) : путь к файлу, который хотим спарсить.
    path_to_db (str) : путь к БД в которую хотим поместить расписание.
    id_days (str) : дата на которую было составлено расписание в формате
        dd.mm.yyyy).
    """

    table = parse_table(path_day)

    # Помещаем значения списка в существующую базу данных SQLite
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        number: int = 0
        # Помещаем значения списка в таблицу
        for row in table:
            # Преобразуем список в кортеж перед добавлением номера строки
            row_with_number = tuple([id_days] + [number] + row)
            cursor.execute(
                '''INSERT INTO day_detailed 
                (id_days, number, ab, wb_title, fact, fix) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                row_with_number)
            number += 1
        # Сохраняем изменения
        conn.commit()