from src.db_querys.set.loading_schedule import loading_schedule
from src.db_querys.get.get_days_from_db import get_days_from_db
from src.db_querys.set.add_db_days import add_db_days
from src.db_querys.get.extract_db import extract_db
from src.organizer.links import path_to_db
import datetime


def add_day_schedule(date: str, path_schedule: str, limited_status: str = 'indefinite', first_launch: int = 0):
    """ Добавляет новое расписание в таблицы БД days и day_wb. Функция сама
    определяет id и version нового добавляемого расписания (увеличивая их на 1)

    date (str) - дата по которой нужно добавить расписание в формате
        'dd.mm.yy'.
    path_schedule (str) - путь к excel файлу с расписанием.
    limited_status (str) - статус режима ограниченной функциональности см. подробнее в модуле db_install.
    first_launch (int) - это первый запуск orgApp за день? - тогда 1.
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
        # Находим id_days последнего расписания в таблице days.
        last_id: list = extract_db(select_column='MAX(id_days)',
                               path_db=path_to_db, table_name='days')
        # Если добавляемое расписание - самое первое за все время.
        if last_id[0][0] == None:
            id_days = 1
            version = 1
        # Если добавляемое расписание самое первое только за сегодня.
        else:
            id_days = last_id[0][0] + 1
            version = 1

    else:
        id_days = days_db_list[0] + 1
        version = days_db_list[2] + 1
    # Добавляем новое расписание в БД, табл. days
    add_db_days(date, version, time_change, limited_status, first_launch)
    # Добавляем новое расписание в БД, табл. day_wb
    loading_schedule(id_days, path_schedule)


if __name__ == '__main__':
    # TODO: Протестировать функцию
    pass