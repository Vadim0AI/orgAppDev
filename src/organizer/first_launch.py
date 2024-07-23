from move_to_history import move_to_history
from check_availability_day import check_availability_day
from src.db_querys.get.checking_enough_time import checking_enough_time
import shutil
from src.db_querys.get.extract_db import extract_db
from src.organizer.links import path_to_db
from datetime import datetime


# TODO: !!! В процессе изменения функции

def first_launch(path_to_history, path_to_now, path_to_future,
                 path_d_future, path_d_now, name_day):
    """ Перемещает старые расписания в папку history. Перемещает расписание
    на сегодня из now в папку future. Проверяет, нужно ли включить режим
    ограниченной функциональности. """

    # Переместить все файлы Day из папки now в папку history
    move_to_history(path_to_now, path_to_history)
    # Проверяем факт режима ограниченной функциональности
    #   Проверить наличие файла Day с таким названием в папке future
    file_exists = check_availability_day(name_day, path_to_future)

    today_dd_mm_yy = datetime.today()
    today_dd_mm_yy = today_dd_mm_yy.strftime('%d.%m.%y')
    where_query = f'date = {today_dd_mm_yy}'

    # Проверяем включен ли режим ограниченной функциональности и его тип
    # TODO: 
    # Обратиться к БД и делаем запрос на получение статуса first_load за сегодня
    # ??? Это список кортежей должен получиться?
    first_load_status: list = extract_db(select_column='first_load', path_db=path_to_db, table_name='days', where_condition=where_query)

    # TODO:см. Как записываются first_load в БД по умолчанию?
    if first_load_status

    # Перемещаем нужный файл Day из папки future в папку now
    shutil.move(path_d_future, path_d_now)



