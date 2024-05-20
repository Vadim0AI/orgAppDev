from datetime import datetime

def get_name_day(date='today'):
    """ Выдает строку с именем файла Day исходя из даты.

    date - по умолчанию 'today', т.е. получает имя исходя из сегодняшней даты;
        в иных случаях строка даты в формате 'dd.mm.yyyy'
    :return (name_day) - строку в формате 'Day_dd_mm_wd' (wd - это день
    недели в краткой записи)
    """
    if date == 'today':
        today = datetime.now()
    else:
        # Преобразовываем строку даты в объект datetime
        today = datetime.strptime(date, '%d.%m.%Y')

    # Получаем имя дня недели в краткой записи (Mon, Tue, etc.)
    day_name = today.strftime('%a')

    # Форматируем дату в строку 'Day_dd_mm_wd'
    name_day = f'Day_{today.strftime("%d_%m")}_{day_name}'

    return name_day

# Примеры использования:
# print(get_name_day())  # Получить имя для сегодняшней даты
# print(get_name_day('12.05.2024'))  # Получить имя для определенной даты