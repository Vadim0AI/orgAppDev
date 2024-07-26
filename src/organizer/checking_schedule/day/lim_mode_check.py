from src.organizer.links import path_to_db
from src.shared.get_dct_from_list_tuple import get_dct_from_list_tuple
from src.organizer.get_wb_settings_dct import get_wb_settings_dct


def lim_mode_check(shedule: list, all_wb: list) -> bool:
    '''
    Проверяет, что в расписании нет запрещенных режимом ограниченной функциональности блоков.

    Параметры:
    shedule (list) - список кортежей, где каждый кортеж - это РБ, причен не атомарный блок в 5 мин, а имено РБ.
    all_wb (list) - список кортежей РБ из талблицы 'wb' БД. Каждый кортеж - это рабочий блок и все соответсвующие ему настройки (все поля таблицы).

    Если в settings РБ, добавленного в расписание содержится настройка и соответсвующее значение "lim_mode : limited_1", то функция вернет False - это значит, что расписание не прошло проверку. Такие РБ нельзя добавлять в расписание, при активном режиме ограниченной функциональности.

    Return:
    (bool) - Если True - значит проверка пройдена успешно - в расписании нет запрещенных РБ.
    '''

    # Преобразуем all_wb в словарь: в качесвте ключа - title.
    all_wb: dict = get_dct_from_list_tuple(lst_tpl=all_wb, key_index=2)

    # Перебираем РБ (в shedule).
    for work_block in shedule:
        title = work_block[3]
        # По title находим соответсвующий РБ в словаре и получаем его settings.
        settings = all_wb[title][6]
        # Преобразуем settings в словарь.
        settings = get_wb_settings_dct(settings)
        # Проверяем условие: есть ли насройка 'limited_1', если да - то возвращаем False.
        if settings['lim_mode'] == 'limited_1':
            return False
    return True # Все РБ расписания проверены - в них нет РБ с ограничениями.
