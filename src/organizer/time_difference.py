def time_difference(start, end):
    # Разбиваем время на часы и минуты
    start_hours, start_minutes = map(int, start.split(':'))
    end_hours, end_minutes = map(int, end.split(':'))

    # Вычисляем разницу в минутах
    total_start_minutes = start_hours * 60 + start_minutes
    total_end_minutes = end_hours * 60 + end_minutes
    difference_minutes = total_end_minutes - total_start_minutes

    # Преобразуем разницу обратно в часы и минуты
    difference_hours = difference_minutes // 60
    difference_minutes %= 60

    # Форматируем результат
    result = "{:02d}:{:02d}".format(difference_hours, difference_minutes)
    return result