import sqlite3
from datetime import datetime
from src.organizer.links import path_to_db


def where_now_wb(id_days):
    """ Определяет какой сейчас РБ и возвращает данные по нему из БД

    id_day (int): уникальный идентификатор расписания по которому делает
    проверку

    return (tuple):
    wb_row (tuple): возвращает все данные текущего РБ в расписании из ДБ
    delta_sec (int): время в секундах, до начала следующего РБ в расписании
    """

    # Получить список с текущим расписанием по РБ;
    # -- Подключаемся к базе данных SQLite
    conn = sqlite3.connect(path_to_db)
    #   Создаем объект курсора
    cursor = conn.cursor()
    # -- Выполняем SQL-запрос для выборки данных
    cursor.execute('SELECT * FROM day_wb WHERE id_days = ? ORDER BY number '
                   'ASC', (id_days,))
    # -- Получаем расписание в виде отсортированного списка кортежей
    day_schedule = cursor.fetchall()

    # Получить текущее время в секундах;
    now_time = datetime.now()
    now_time = ((now_time.hour * 60) + now_time.minute) * 60 + now_time.second

    # Найти соответсвующий РБ в списке;
    for wb_row in day_schedule:
        # если wb sleep
        if wb_row[3] == 'sleep':
            return 'sleep'
        # Иначе, извлечь wb
        wb = wb_row[2]
        # Преобразовать wb в datetime объект
        wb = datetime.strptime(wb, "%H:%M")
        # Получаем время начала wb в секундах (часы тоже превращаем в секунды)
        # + 1 секунда в конце, для того, чтобы отличать начало нового РБ и
            # окончание другого
        wb_from = (((wb.hour * 60) + wb.minute) * 60) + 1
        # Преобразуем duration в секунды - получаем время окончания wb
        duration = wb_row[6] # формат: 'hh:mm'
        duration = datetime.strptime(duration, "%H:%M")
        wb_to = wb_from + ((duration.hour * 3600) + duration.minute * 60)
        # Проверить на основе wb и duration, входит ли настоящее время в
        #   этот диапазон
        if wb_from <= now_time and now_time <= wb_to:
            # Вычислить delta_sec для вывода количества секунд до следующего РБ
            delta_sec = wb_to - now_time
            return wb_row, delta_sec


if __name__ == '__main__':
    id = 2
    a = where_now_wb(id)
    print(a)
