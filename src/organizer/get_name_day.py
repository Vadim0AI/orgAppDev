from datetime import datetime, timedelta

def get_name_day(date='today'):
    """ Выдает строку с именем файла Day исходя из даты.

    date - по умолчанию 'today', т.е. получает имя исходя из сегодняшней даты;
        в иных случаях строка даты в формате 'dd.mm.yyyy'
    :return (name_day) - строку в формате 'Day_dd_mm_wd' (wd - это день
    недели в краткой записи)
    """
    if date == 'today':
        my_date = datetime.now()
    elif date == 'tomorrow':
        my_date = (datetime.now() + timedelta(days=1))
    else:
        # Преобразовываем строку даты в объект datetime
        my_date = datetime.strptime(date, '%d.%m.%Y')

    # Получаем имя дня недели в краткой записи (Mon, Tue, etc.)
    day_name = my_date.strftime('%a')

    # Форматируем дату в строку 'Day_dd_mm_wd'
    name_day = f'Day_{my_date.strftime("%d_%m")}_{day_name}.xlsx'

    return name_day


if __name__ == '__main__':
    # Примеры использования:
    print(get_name_day())  # Получить имя для сегодняшней даты
    print(get_name_day('12.05.2024'))  # Получить имя для определенной даты
    print(get_name_day('tomorrow'))  # Получить имя для завтрашней даты
