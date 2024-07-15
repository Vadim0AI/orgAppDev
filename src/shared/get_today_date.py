from datetime import datetime


def get_today_date():
    """ Возвращает (str) сегодняшнюю дату в формате 'dd.mm.yy' """

    # Получаем текущую дату
    today = datetime.now()

    # Форматируем дату в нужный формат 'dd.mm.yy'
    formatted_date = today.strftime('%d.%m.%y')

    return formatted_date
