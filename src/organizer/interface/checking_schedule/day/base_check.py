from src.shared.xlsx_utils.num_rows_xlsx import num_rows_xlsx
from src.organizer.day_ab_to_wb import day_ab_to_wb, calc_duration
from src.shared.xlsx_utils.parse_table import parse_table
from datetime import datetime


def base_check(template_path, day_path, sheet_name, start_time, sleep_time,
               min_wb: int) -> bool:
    """
     ...
     min_wb (int) - минимальное приемлемое кол-во РБ в расписании;
     ...
     """
    # TODO: [~] base_check()
    # Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    #   этого обращаемся к детализированным версиям расписаний;
    if not num_rows_check(template_path, day_path, sheet_name):
        return False

    # Парсим таблицу с расписанием в список
    #   (получаем расписание по РБ);
    day_ab = parse_table(day_path)
    day_wb = day_ab_to_wb(day_ab)
    day_wb = calc_duration(day_wb)
    # Первый блок - 'start day' и он не раньше 4:00
    if not start_day_check(day_wb, start_time):
        return False
    # Последний блок - 'sleep' и он не позднее 23:00
    if not start_day_check(day_wb, sleep_time):
        return False
    # Проверяем, что нет пустых РБ между началом и концом расписания и все
    #   РБ расписания есть в БД;

    # Проверка: кол-во РБ в расписании не менее пяти (min_wb);
    if not len(day_wb) > min_wb:
        return False
    # В расписании должен быть РБ "plan day", длительностью не менее десяти
    #   минут;
    return True


def num_rows_check(template_path, day_path, sheet_name):
    """ Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    этого обращаемся к детализированным версиям расписаний """
    num_rows_temp = num_rows_xlsx(template_path, sheet_name)
    num_rows_day = num_rows_xlsx(day_path, sheet_name)
    if num_rows_temp == num_rows_day:
        return True
    else:
        return False


def start_day_check(day_wb: list, start_time: str = '4:00') -> bool:
    """
    ...
    # TODO: Дописать многострочный комментарий
    Проверяет, что первый рабочий блок - 'start day' и он не раньше start_time.
    ...
     """
    # Преобразовать start_time и first_wb_time в формат datetime для сравнения
    start_time = datetime.strptime(start_time, "%H:%M")
    first_wb_time = datetime.strptime(day_wb[0][1], "%H:%M")
    # Проверяем, что first_wb_time не раньше start_time
    if day_wb[0][2] == 'start day' and (first_wb_time > start_time):
        return True
    else:
        return False


def end_day_check(day_wb: list, sleep_time: str = '4:00') -> bool:
    """
        ...
        # TODO: Дописать многострочный комментарий
        Проверяет, что последний рабочий блок - 'sleep' и он не позже
        sleep_time.
        ...
         """
    # Преобразовать start_time и first_wb_time в формат datetime для сравнения
    sleep_time = datetime.strptime(sleep_time, "%H:%M")
    last_wb_time = datetime.strptime(day_wb[len(day_wb)][1], "%H:%M")
    # Проверяем, что first_wb_time не раньше start_time
    if day_wb[len(day_wb)][2] == 'sleep' and (last_wb_time < sleep_time):
        return True
    else:
        return False


def check_

