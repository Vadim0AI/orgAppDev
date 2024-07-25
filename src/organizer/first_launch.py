from move_to_history import move_to_history
from check_availability_day import check_availability_day
import shutil
from src.db_querys.get.extract_db import extract_db
from src.organizer.links import path_to_db
from datetime import datetime


def first_launch(path_to_history: str, path_to_now: str,
                 path_d_future: str, path_d_now: str):
    """ Перемещает старые расписания в папку history. Перемещает расписание
    на сегодня из now в папку future. Функция автоматически не станет запускаться, если уже запускалась сегодня (в нее встроена проверка). """

    # Проверяем, был ли выполнен first_launch ранее за сегодня, если да - пропускаем выполненеие функции.
    today_dd_mm_yy = datetime.today()
    today_dd_mm_yy = today_dd_mm_yy.strftime('%d.%m.%y')
    where_query = f'date = {today_dd_mm_yy}'
    first_launch_status: list = []
    # fl_from_db - список кортежей, каждый кортеж с одним значением столбца first_launch извлекаем его из БД days
    fl_from_db: list = extract_db(select_column='first_launch', path_db=path_to_db, table_name='days', where_condition=where_query)
    for tpl in fl_from_db:
        first_launch_status.append(tpl[0])
    if 1 in first_launch_status:
        return None

    # Переместить все файлы Day из папки now в папку history.
    move_to_history(path_to_now, path_to_history)

    try:
        # Перемещаем файл из папки future в папку now
        shutil.move(path_d_future, path_d_now)
    except FileNotFoundError:
        print(f"Файл {path_d_future} не найден.")
