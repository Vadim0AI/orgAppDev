from src.organizer.time_difference import time_difference
import sqlite3



def day_ab_to_wb(day_ab: list) -> list:
    """
    Преобразует длинную версию расписания по ab в более емкую по wb.

    Если у соседних ab одинаковое имя задачи, то создается элемент списка
    (тоже список), который содержит время самого первого ab с общим именем
    задачи, и само это имя задачи. Затем этот элемент
    добавляется в список day_wb.
    """

    day_wb: list = []
    last_task: str = ''

    for ab in day_ab:
        name_task = ab[1]
        if name_task == last_task:
            pass
        else:
            last_task = name_task
            start_time = ab[0]
            wb = [start_time, last_task, ab[2], ab[3]]
            day_wb.append(wb)
    del day_wb[len(day_wb)-1]
    return day_wb


def calc_duration(day_wb: list) -> list:
    """ Возвращает список расписания day_wb с добавлением number и duration

    duration в формате 'hh:mm'
    """
    number_wb = 0
    for wb in day_wb:
        next_number_wb = number_wb + 1
        # Защита от выхода за пределы списка day_wb
        if next_number_wb < len(day_wb):
            # Время начала текущего РБ
            start = wb[0]
            # Время начала следующего РБ
            end = day_wb[next_number_wb][0]
            duration = time_difference(start, end)
        else:
            start = wb[0]
            end = '24:00'
            duration = time_difference(start, end)
        wb.append(duration)
        wb.insert(0, number_wb)
        number_wb += 1
    day_wb_duration: list = day_wb
    return day_wb_duration


def day_wb_in_db(db: str, id_days: int, day_ab):
    """ Помещает список day_wb в таблицу базы данных day_wb """
    day_wb = day_ab_to_wb(day_ab)
    day_wb = calc_duration(day_wb)
    # Удаляем первое значение т.к. оно всегда будет с пустым title т.к. первый
    #   РБ расписания должен быть не с 0:00
    del day_wb[0]
    # Запись в БД
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        for row in day_wb:
            row = tuple([id_days] + row)
            cursor.execute(
                '''INSERT INTO day_wb 
                (id_days, number, wb_start, wb_title, fact, fix, duration) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', row)
        # Сохраняем изменения
        conn.commit()
