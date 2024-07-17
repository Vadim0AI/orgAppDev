from src.organizer.checking_schedule.day import base_check
from src.organizer.links import path_day_temp
from src.organizer.get_unique_wb import get_unique_wb
from src.organizer.get_wb_settings_dct import get_wb_settings_dct
from src.organizer.wb_settings_check import wb_settings_check
from shared.filtering_list_tpl import filtering_list_tpl


# TODO: Получеть dict[tuple] можно при помощи get_dct_from_list_tuple()

def dur_shift_check(old_shedule: list[tuple], new_shedule: list[tuple], all_wb: dict[tuple]) -> bool:
    """  
    Проверяет РБ для которых в БД табл. wb указаны специальные настройки, ограничивабщие сдвиги и изменение длительности. Если условия длительности и/или сдвигов нарушены - возвращает False.

    # TODO: !!! Пока реализовано только для настроек 
    #   'shift : fix-right | duraton : low-fix'

    'shift : fix-right | duraton : low-fix' - эта настройка означает, что сдвигать РБ можно только дальше по времени (либо не сдвигать), а общее время РБ можно только уменьшать или оставить прежним.

    В интервале от начала одного РБ этого типа, до начала другого РБ этого типа не должно быть длительности большей, чем длительность первого РБ + свободная длительность предыдущих РБ такого типа.

    Parameters:
    old_shedule (list[tuple]): старое расписание (содержится в БД табл. dat_wb).
    new_shedule (list[tuple]): новое расписание (до этой проверки содержится пока только в excel и извлекается из него).
    all_wb (dict[tuple]): словарь кортежей из БД табл. wb. (Все рабочие блоки и их настройки).
    
    Returns:
    check_result (bool): Результат проверки
    """

     # Получаем словари уникальных РБ для старого и нового расписаний. В значениях по ключу содержится (dur_uniq_wb, count_uniq_wb)
    old_unique_wb = get_unique_wb(old_shedule)
    new_unique_wb = get_unique_wb(new_shedule)

    # Это шаблон проверяемой настройки
    template_settings: str = 'shift : fix-right | duraton : low-fix'
    # Превращаем его в словарь. Где ключ - это тип настройки, а значение - это кортеж с значениями настройки).
    template_settings: dict[tuple] = get_wb_settings_dct(template_settings)

    # Решаем - проверять ли дальше этот РБ на сдвиги и длительность. Для этого узнаем есть ли особая настройка template_settings у РБ. Перебираем словарь уникальных РБ нового расписания и проверяем, соответсвует ли РБ настройкам template_settings.
    # TODO: Пока функция просто сравнивает словари - сложные комбинации и пересечения настроек не учитываются.
    for unique_wb in new_unique_wb:
        # Получаем настройку РБ
        wb_setting = get_wb_settings_dct(all_wb[unique_wb][6])
        if wb_settings_check(template_settings, wb_setting):
            # выполняем проверку по этому РБ
            # TODO: Возможно цикл сверху стоит выделить в отдельную функцию / генератор / итератор.
            




            # 3. Извлекаем из старого расписания РБ только одного типа. Делаем то же самое и для нового расписания.
            # TODO: Написать для этого отдельную функцию
            one_type_wb_old = 
            for work_block in 

            
            # 4. Получаем список интервалов для старого расписания с длительностью нужного РБ в них.
            # 5. Проходимся по списку с уникальными РБ нового расписания и проверяем вхождение в
            #   интевал старого расписания, для тех РБ которые входят в этот интервал суммируем 
            #   длительность и сверяем ее с длительностью РБ интервала (! не дительность самого 
            #   интервала) из старого расписания. 
            # 6. Если длительность старого меньше, чем сумма этих РБ + free_duration 
            #   - выводим ошибку (False), а также данные о месте ошибки.
            #   Иначе - вычисляем разницу и сохраняем в free_duration. 
            #   Изначально free_duration был установлен в 0.
            # 7. Продолжаем так, пока не пройдемся по всем РБ нового расписания этого типа.
            # 8. Затем возвращаемся к п.2, пока не пройдем так полный список уникальных РБ.
            # 9. Если все ок - то возвращаем True.





