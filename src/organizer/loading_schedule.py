from src.shared.xlsx_utils.parse_table import parse_table
from day_ab_to_wb import day_wb_in_db



def loading_schedule(db, id_days, path_d_now):
    """ Парсит расписание на день из excel и помещает в БД. """

    day_ab = parse_table(path_d_now)
    # Трансформируем список с расписанием по АБ в формат РБ и помещаем его в
    #   таблицу БД "day_wb"
    day_wb_in_db(db, id_days, day_ab)