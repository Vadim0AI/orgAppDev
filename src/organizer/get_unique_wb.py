from shared.manipulate_str_time import sum_str_time


def get_unique_wb(day_wb: list[tuple]) -> dict:
    """
    Возвращает словарь всех уникальных РБ расписания и суммарную
    длительность по каждому уникальному РБ, а также их кол-во в расписании. 
    'wb_title : (duration, number)'

    Parameters:
    day_wb (list[tuple]): список кортежей с расписанем на день из БД таблицы day_wb
    
    Returns:
    unique_wb (dict):

    unique_wb[title] = (dur_uniq_wb, count_uniq_wb)
    Ключ - title рабочего блока. dct[] = (длительность РБ, кол-во РБ)
    dur_uniq_wb (str): 'hh:mm'
    count_uniq_wb (int)

    """

    unique_wb: dict

    # Пройтись по списку расписания
    for work_block in day_wb:
        wb_title = work_block[3]
        # Получаем длительность текущего РБ в итерации.
        duration = work_block[6]

        # Проверяем, был ли этот РБ уже внесен в unique_wb.
        if wb_title in unique_wb:
            dur_uniq_wb = duration
            count_uniq_wb = 1
        else:
            # Получаем внесенную в словарь общую длительность РБ за день.
            dur_uniq_wb = unique_wb[wb_title][0]
            # Прибавляем к ней новое значение;
            # sum_str_time() - складывает время в строках в формате 'hh:mm'.
            dur_uniq_wb = sum_str_time(dur_uniq_wb, duration)

            # Получаем кол-во РБ данного типа в словаре и прибавляем +1.
            count_uniq_wb = unique_wb[wb_title][1]
            count_uniq_wb += 1

        # Обновлем значения словаря
        unique_wb[wb_title] = (dur_uniq_wb, count_uniq_wb)
    return unique_wb
