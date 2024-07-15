from src.shared.sum_str_time import sum_str_time


def get_unique_wb(day_wb: list) -> dict:
    """
    Возвращает словарь всех уникальных РБ расписания и суммарную
    длительность по каждому уникальному РБ, а также их кол-во в расписании. 
    'wb_title : (duration, number)'

    Parameters:
    day_wb (list): список кортежей с расписанем на день из БД таблицы day_wb
    
    Returns:
    unique_wb (dict):

    unique_wb[title] = (dur_uniq_wb, count_uniq_wb)
    Ключ - title рабочего блока. dct[] = (длительность РБ, кол-во РБ)
    dur_uniq_wb (str): 'hh:mm'
    count_uniq_wb (int)

    """

    unique_wb: dict

    # 1. Пройтись по списку расписания
    for work_block in day_wb:
        wb_title = work_block[3]
        dur_uniq_wb = sum_str_time(one_hh_mm=, two_hh_mm=)

        unique_wb[wb_title] = (dur_uniq_wb, count_uniq_wb)

    

    return unique_wb

