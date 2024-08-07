from src.organizer.checking_schedule.day import base_check
from src.organizer.links import path_day_temp
from src.organizer.get_unique_wb import get_unique_wb
from src.organizer.get_wb_settings_dct import get_wb_settings_dct
from src.organizer.wb_settings_check import wb_settings_check
from src.shared.filtering_list_tpl import filtering_list_tpl
from datetime import time, datetime
from src.shared.manipulate_str_time import manipulate_str_time


# TODO: Пока функция get_wb_settings_dct() просто сравнивает словари - сложные комбинации и пересечения настроек не учитываются.


def dur_shift_check(old_schedule: list[tuple], new_schedule: list[tuple], all_wb: dict[tuple]) -> list[bool, str]:
    """  
    Проверяет РБ для которых в БД табл. wb указаны специальные настройки, ограничивабщие сдвиги и изменение длительности. Если условия длительности и/или сдвигов нарушены - возвращает False.

    # TODO: !!! Пока реализовано только для настроек 
    #   'shift : fix-right | duraton : low-fix'

    'shift : fix-right | duraton : low-fix' - эта настройка означает, что сдвигать РБ можно только дальше по времени (либо не сдвигать), а общее время РБ можно только уменьшать или оставить прежним.

    В интервале от начала одного РБ этого типа, до начала другого РБ этого типа не должно быть длительности большей, чем длительность первого РБ + свободная длительность предыдущих РБ такого типа.

    Parameters:
    old_schedule (list[tuple]): старое расписание (содержится в БД табл. dat_wb).
    new_schedule (list[tuple]): новое расписание (до этой проверки
    содержится пока только в excel и извлекается из него) При этом это
    должны быть не АБ а РБ.
    all_wb (dict[tuple]): словарь кортежей из БД табл. wb. (Все рабочие блоки и их настройки).
    
    Returns:
    check_result list[bool, str]: Результат проверки: [True/False, 'Текст для уведомления о результатах проверки']
    """

    # Получаем словари уникальных РБ для старого и нового расписаний. В значениях по ключу содержится (dur_uniq_wb, count_uniq_wb)
    old_unique_wb = get_unique_wb(old_schedule)
    new_unique_wb = get_unique_wb(new_schedule)

    # Это шаблон проверяемой настройки
    template_settings: str = 'shift : fix-right | duraton : low-fix'
    # Превращаем его в словарь. Где ключ - это тип настройки, а значение - это кортеж с значениями настройки).
    template_settings: dict[tuple] = get_wb_settings_dct(template_settings)

    # Решаем - проверять ли дальше этот РБ на сдвиги и длительность.
    for unique_wb in new_unique_wb:
        # Получаем настройку РБ
        wb_setting = get_wb_settings_dct(all_wb[unique_wb][6])
        # Сравнивает шаблон настроек template_settings и реальную настройку РБ
        if wb_settings_check(template_settings, wb_setting):
            
            # Преобразуем строки времени в объекты datetime.time
            dur_old = datetime.strptime(old_unique_wb[unique_wb][0], '%H:%M').time()
            dur_new = datetime.strptime(new_unique_wb[unique_wb][0], '%H:%M').time()

            # Проверяем общую длительность РБ
            if dur_new > dur_old:
                return [False, f'Общая длительность РБ {unique_wb} ({new_unique_wb[unique_wb][0]}) превышает значение в страром расписании ({old_unique_wb[unique_wb][0]})']

            # Получаем списки интервалов для одного РБ.
            old_interval_wb: list[tuple] = filtering_list_tpl(input_lst_tpl=old_schedule, index_filter=3, value_filter=unique_wb[3])
            new_interval_wb: list[tuple] = filtering_list_tpl(input_lst_tpl=new_schedule, index_filter=3, value_filter=unique_wb[3])
            
            # Длительность РБ которая перемещается в следующий(ие) РБ, если предыдущем интервале старого расписания длительности стало меньше.
            moving_duration: str = '00:00'
            
            # Перебираем интервалы старого расписания
            for old_wb_index in range(len(old_interval_wb)):
                
                # Сумма длительнсти рабочих блоков нового расписания, которые находятся внутри текущего интервала старого расписания.
                new_dur_inside: str = '00:00'

                # Перебираем интервалы нового расписания
                for new_wb_index in range(len(new_interval_wb)):
                    work_block_new = new_interval_wb[new_wb_index]

                    # Преобразуем строки времени в объект datetime.time
                    # Время начала рабочего блока из нового расписания
                    start_time_new = datetime.strptime(work_block_new[2], '%H:%M').time()
                    # Время окончания рабочего блока из нового расписания
                    end_time_new_str: str = manipulate_str_time(start_time_new, work_block_new[6], '+')
                    end_time_new_obj = datetime.strptime(end_time_new_str, '%H:%M').time()
                    # Время начала интервала старого расписания
                    start_time_old = datetime.strptime(old_interval_wb[old_wb_index][2], '%H:%M').time()
                    # Время окончания интервала старого расписания
                    end_time_old = datetime.strptime(old_interval_wb[old_wb_index+1][2], '%H:%M').time()

                    # Выполняем проверку на вхождение
                    if (start_time_old <= start_time_new) and (start_time_new <= end_time_old):

                        # Проверяем, находится ли РБ из нового расписания на стыке нескольких интервалов старого расписания.
                        if end_time_new_obj > end_time_old:

                            # Создаю новый РБ на основе текущего, с началом равным окончанию интервала и с остаточной длительностью.
                            created_wb: list = list(work_block_new)
                            # Изначальное время начала РБ 'hh:mm'
                            old_beginnin_wb: str = work_block_new[2]    
                            created_wb[2] = old_interval_wb[old_wb_index+1]
                           
                            # Длительность РБ в рамках текущего интервала = Время начала следующего интервала - Изначальное время начала РБ. 'hh:mm'.
                            dur_wb_cur_interval: str = manipulate_str_time(created_wb[2], old_beginnin_wb, '-')
                             # Остаточная длительность РБ = Изначальная длительность РБ - Длительность РБ в рамках текущего интервала. 'hh:mm'
                            created_wb[6] = manipulate_str_time(work_block_new[6], dur_wb_cur_interval, '-')
                            created_wb = tuple(created_wb)
                            # Вставляем в new_interval_wb (список кортежей с РБ одного типа нового расписания) новый РБ, сразу после текущего.
                            new_interval_wb.insert(new_wb_index+1, created_wb)

                            # Считаю длительность первой части текущего РБ и прибавляю ее к new_dur_inside
                            first_part_dur = manipulate_str_time(old_interval_wb[old_wb_index+1][2], work_block_new[2], '-')
                            new_dur_inside = manipulate_str_time(new_dur_inside, first_part_dur, '+')
                        else:
                            # Добавляю значение к new_dur_inside
                            new_dur_inside = manipulate_str_time(new_dur_inside, work_block_new[6], '+')
                        
                
                # Разрешенная суммарная длительность рабочих блоков в текущем интервале.
                allowed_dur = manipulate_str_time(old_interval_wb[old_wb_index][6], moving_duration, '+')

                # Проверяем, было ли нарушено правило настройки для текущего интервала старого расписания. Если new_dur_inside больше чем (длительность_РБ_старого_расписания + moving_duration), то False.
                if datetime.strptime(new_dur_inside, '%H:%M').time() > datetime.strptime(allowed_dur, '%H:%M').time():
                    return [False, f'Превышена длительность рабочих блоков(а) в интервале с {old_interval_wb[old_wb_index][2]}, до {old_interval_wb[old_wb_index+1][2]}']

                # Обновляем moving_duration. Для этого moving_duration = длительность_РБ_старого_расписания + moving_duration - new_dur_inside
                moving_duration = manipulate_str_time(moving_duration, new_dur_inside, '-')
                moving_duration = manipulate_str_time(moving_duration, old_interval_wb[old_wb_index][6], '+')

    return [True, '']   # Если все ок - возвращаем True.      
