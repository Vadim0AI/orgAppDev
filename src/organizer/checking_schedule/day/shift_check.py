


def shift_check():

    # Посчитать кол-во РБ
    # Один большой РБ разделяется на несколько меньших
    # Более простой принцип:
    # Находится в прошлом расписании сначала ближайший особый РБ, получаем его
    #   длительность и время начала. Затем следующий.
    # Все - далее просто нельзя начинать РБ этого типа раньше этого времени, 
    # при этом сдвигать другие РБ этого типа ближе можно, но не раньше этого времени.
    # 

    # В интервале от начала одного РБ этого типа, до начала другого РБ этого типа
    #   не должно быть длительности большей, чем длительность первого РБ + свободная  
    #   длительность предыдущих РБ такого типа.
    
    # 1. Получаем 1) список со старым расписанием на день; 2) список уникальных РБ с кол-вом
    #   и длительностью, 3) список настроек РБ из БД, 4) список с новым расписанием на день;
    # 2. Проходим по списку уникальных РБ и сверяем его с БД wb, там где есть в settings
    #   'shift : right | duraton : fix' выполняем следующий алгоритм для выбранного РБ
    # 3. Получаем из нового расписания список только из этих РБ в соответсвии с их порядком,
    #   а также отдельный такой список для старого расписания.
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



    pass
