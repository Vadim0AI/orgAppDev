from src.organizer.loading_schedule import loading_schedule
from src.organizer.get_days_from_db import get_days_from_db
import datetime


def add_day_schedule(date: str, path_schedule: str, first_load: bool = False):
    """ Добавляет новое расписание в таблицы БД days и day_wb

    date (str) - дата по которой нужно добавить расписание в формате
    'dd.mm.yy'.
    version (str) - версия расписания не день в формате (пример) '1.2.1'.
        Применимо для получения прошлых версий расписаний для аналитики,
        возврата к старым шаблонам и пр. Также поддерживает формат 'last' -
        для получения последней версии расписания. И 'first' для первой.
    """

    # Получить текущее время (для time_change) в формате 'hh:mm:ss dd.mm.yy'
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S %d.%m.%y')
    # Получить id_days по которому будем добавлять расписание в таблицу БД
    #   day_wb
    # TODO: Протестировать,
    #   нужно ли здесь [0] - будет ли всегда список кортежей, или просто кортеж
    days_db_list = get_days_from_db(date)[0]
    if len(days_db_list) == 0:
        id_days = 1
    else:
        id_days = days_db_list[0]

    # Добавляем новое расписание в БД, табл. days

    # Добавляем новое расписание в БД, табл. day_wb
    loading_schedule(id_days, path_schedule)

    #

    # Обработать:
        # id_days
        # date
        # version
        # time_change
        # enough_time
        # first_load



    pass