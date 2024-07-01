import sqlite3
from src.organizer.links import path_to_db


def add_db_days(date: str, version: str, time_change: str, enough_time: int,
                first_load: int) -> None:
    """ Добавляет в БД табл. days новую запись

    date (str) - дата на которую запланировано расписание в формате 'dd.mm.yy'.
    version (str) - версия расписания. Например, '1.2'.
    time_change (str) - hh:mm:ss dd.mm.yy.
    enough_time (int) - время, затраченное на составление этой версии
        расписания.
    first_load (int) - 0 или 1, факт того, было ли за сегодня загружено
    расписание на день (1, если да).
    """

    with sqlite3.connect(path_to_db) as conn:
        # Создаем курсор
        cursor = conn.cursor()
        # Вставка данных в таблицу
        cursor.execute(
            'INSERT INTO days (date, version, time_change, enough_time, '
            'first_load) VALUES (?, ?, ?, ?, ?)',
            (date, version, time_change, enough_time, first_load))
        # Фиксация изменений
        conn.commit()


if __name__ == '__main__':
    add_db_days(date='28.06.24', version='1.0',
                time_change='21:28:56 28.06.24',
                enough_time=0, first_load=0)
