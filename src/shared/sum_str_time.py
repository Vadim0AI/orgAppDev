def sum_str_time(one_hh_mm: str, two_hh_mm: str):
    """ 
    Суммирует время полученное из двух строк формата 'hh:mm', 
    возвращает в этом же формате.
    """
    # Разделяем строки на часы и минуты
    hh1, mm1 = map(int, one_hh_mm.split(':'))
    hh2, mm2 = map(int, two_hh_mm.split(':'))
    
    # Суммируем часы и минуты
    total_mm = mm1 + mm2
    total_hh = hh1 + hh2 + total_mm // 60  # Учитываем переполнение минут
    total_mm = total_mm % 60
    
    # Форматируем результат в строку 'hh:mm'
    result_hh_mm = f"{total_hh:02d}:{total_mm:02d}"
    
    return result_hh_mm


if __name__ == '__main__':
    print(sum_str_time('02:30', '03:45'))  # Вывод: '06:15'
    print(sum_str_time('11:00', '00:05'))  # Вывод: '11:05'
