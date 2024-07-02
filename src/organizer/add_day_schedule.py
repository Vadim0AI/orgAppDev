from src.organizer.loading_schedule import loading_schedule
from src.organizer.get_days_from_db import get_days_from_db
from src.organizer.add_db_days import add_db_days
import datetime


def add_day_schedule(date: str, path_schedule: str, enough_time: bool = False,
                     first_launch: bool = False):
    """ Добавляет новое расписание в таблицы БД days и day_wb. Функция сама
    определяет id и version нового добавляемого расписания (увеличивая их на 1)

    date (str) - дата по которой нужно добавить расписание в формате
        'dd.mm.yy'.
    path_schedule (str) - путь к excel файлу с расписанием.
    enough_time (bool) - достаточно ли времени было затрачено на составление
        расписания?
    first_launch (bool) - это первый запуск orgApp за день? - тогда True.
        Это нужно, чтобы выполнять одноразовые предварительные действия при
        первом запуске orgApp за день. Если за день есть хотя бы в одной
        записи True по этому полю, то предварительные действия больше делать не
        нужно.
    """

    # Получаем текущее время в формате 'hh:mm:ss dd.mm.yy'.
    time_change = datetime.datetime.now()
    time_change = time_change.strftime('%H:%M:%S %d.%m.%y')
    # Получаем кортеж c записью из БД days по дате, последней версии.
    days_db_list = get_days_from_db(date)
    # Получаем id_days по которому будем
    #   добавлять расписание в таблицу БД day_wb.
    if len(days_db_list) == 0:
        id_days = 1
        version = 1
    else:
        id_days = days_db_list[0]
        version = days_db_list[2]
    # Добавляем новое расписание в БД, табл. days
    add_db_days(date, version, time_change, enough_time, first_launch)
    # Добавляем новое расписание в БД, табл. day_wb
    loading_schedule(id_days, path_schedule)


if __name__ == '__main__':
    # TODO: Протестировать функцию
    pass