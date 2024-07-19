from src.shared.xlsx_utils.num_rows_xlsx import num_rows_xlsx
from src.db_querys.set.day_ab_to_wb import day_ab_to_wb, calc_duration
from src.shared.xlsx_utils.parse_table import parse_table
from datetime import datetime
from src.db_querys.get.extract_db import extract_db


# TODO: Переделать функцию так, чтобы выводился кортеж (bool, str) - строка
#  должна описывать причину(ы), почему расписание не прошло проверку.
def base_check(template_path: str, day_path: str, sheet_name: str,
               start_orgapp: str, sleep_time: str,
               min_wb: int, planning_dur: str, path_db: str,
               wb_table_name: str) -> list:
    """
     ...
     Используется для проверки расписания на завтра при его составлении.
     А также, как основа для
     Если True - значит все хорошо.

    template_path (str): путь к excel-фалу с шаблоном расписания на день.
    day_path (str): путь к проверяемому excel-фалу с расписанием на день.
     min_wb (int): минимальное приемлемое кол-во РБ в расписании;
     planning_dur (str): минимальная длительность РБ "plan day" в формате
        "hh:mm";
     sheet_name (str): имя листа excel для детального расписания на день;
     wb_table_name (str): имя таблицы в БД для списка всех РБ;
     ...
     """
    # Результат проверки (пока пустой)
    check_result: list = [True, '']

    # Парсим таблицу с расписанием в список
    #   (получаем расписание по РБ);
    day_ab = parse_table(day_path)
    day_wb = day_ab_to_wb(day_ab)
    day_wb = calc_duration(day_wb)
    del day_wb[0]

    if len(day_wb) == 0:
        check_result[0] = False
        check_result[1] = ('Расписание пустое!')
        return check_result

    # TODO: [~] base_check()
    # Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    #   этого обращаемся к детализированным версиям расписаний;
    if not num_rows_check(template_path, day_path, sheet_name):
        check_result[0] = False
        check_result[1] = ('1. Количество строк в расписании не совпадает с '
                           'шаблоном\n')

    # Первый блок - 'start day' и он не раньше start_orgapp (Например, 4:00)
    if not start_day_check(day_wb, start_orgapp):
        check_result[0] = False
        check_result[1] = check_result[1] + ('2. Либо первый блок не "start '
                                             'day", либо он не раньше '
                                             'start_time\n')

    # Последний блок - 'sleep' и он не позднее 23:00
    if not end_day_check(day_wb, sleep_time):
        check_result[0] = False
        check_result[1] = check_result[1] + ('3. Либо последний блок не '
                                             'sleep, либо он позднее 23:00\n')

    # Проверяем, что нет пустых РБ между началом и концом расписания и все
    #   РБ расписания есть в БД;
    all_wb_from_db = extract_db(select_column='title', path_db=path_db,
                        table_name=wb_table_name)
    # all_wb_from_db будет списком с кортежами, которые содержат одиночные
    #   значения - нужно превратить его просто в список значений
    all_wb: list = []
    for sublist in all_wb_from_db:
        for item in sublist:
            all_wb.append(item)
    # Собственно сама проверка
    if not check_wb(day_wb, all_wb):
        check_result[0] = False
        check_result[1] = check_result[1] + ('4. Либо есть пустые РБ между '
                                             'началом и концом расписания '
                                             'или не все РБ расписания есть в '
                                             'БД\n')

    # Проверка: кол-во РБ в расписании не менее десяти (min_wb);
    if not len(day_wb) > min_wb:
        check_result[0] = False
        check_result[1] = check_result[1] + ('5. Кол-во РБ в расписании '
                                             'менее десяти\n')

    # В расписании должен быть РБ "plan day", длительностью не менее десяти
    #   минут;
    if not plan_day_exists(day_wb, planning_dur):
        check_result[0] = False
        check_result[1] = check_result[1] + ('6. В расписании должен быть РБ '
                                             '"plan day", длительностью не '
                                             'менее десяти минут\n')

    if not check_result[0]:
        check_result[1] = 'Расписание содержит ошибки:\n' + check_result[1]

    if check_result[0]:
        check_result = [True, 'Расписание прошло проверку - все ок']

    return check_result


def num_rows_check(template_path, day_path, sheet_name):
    """ Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    этого обращаемся к детализированным версиям расписаний """
    num_rows_temp = num_rows_xlsx(template_path, sheet_name)
    num_rows_day = num_rows_xlsx(day_path, sheet_name)
    if num_rows_temp == num_rows_day:
        return True
    else:
        return False


def start_day_check(day_wb: list, start_orgapp: str = '4:00') -> bool:
    """
    ...
    # TODO: Дописать многострочный комментарий
    Проверяет, что первый рабочий блок - 'start day' и он не раньше start_time.
    ...
     """

    # Преобразовать start_time и first_wb_time в формат datetime для сравнения
    start_orgapp = datetime.strptime(start_orgapp, "%H:%M")
    first_wb_time = datetime.strptime(day_wb[0][1], "%H:%M")
    # Проверяем, что first_wb_time не раньше start_time
    if day_wb[0][2] == 'start day' and (first_wb_time > start_orgapp):
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
    last_wb_time = datetime.strptime(day_wb[len(day_wb)-1][1], "%H:%M")
    # Проверяем, что first_wb_time не раньше start_time
    if day_wb[len(day_wb)-1][2] == 'sleep' and (last_wb_time < sleep_time):
        return True
    else:
        return False


def plan_day_exists(day_wb: list, planning_dur: str) -> bool:
    """
    Проверяет, что в расписании есть РБ "plan day", длительностью не менее
    десяти минут;

    day_wb (list) - расписание, разбитое по РБ;
    planning_dur (str) - минимальная длительность планирования на завтра;
     """
    # Преобразуем строку planning_dur в datetime
    planning_dur = datetime.strptime(planning_dur, "%H:%M")
    # Перебираем расписание и проверяем каждый РБ
    for wb in day_wb:
        if (wb[2] == 'plan day' and
                datetime.strptime(wb[5], "%H:%M") > planning_dur):
            return True
    return False


def check_wb(day_wb: list, all_wb: list):
    """
    Проверяет, что нет пустых РБ между началом и концом расписания и все РБ
    расписания есть в БД;

    day_wb (list): это список с детальным расписанием
    all_wb (list): список с title всех РБ из файла work_blocks.xlsx
    """
    for wb in day_wb:
        if (wb[2] == 0) or (wb[2] not in all_wb):
            return False
    return True
