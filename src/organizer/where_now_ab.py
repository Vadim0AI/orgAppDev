import time
from datetime import datetime, timedelta
import threading

def generate_time_tuples():
    """ Создает кортеж с интервалами времени от 0:00 до 23:55
    с разницей в 5 минут """
    time_tuples = []
    for hour in range(24):
        for minute in range(0, 60, 5):
            time_str = f"{hour:02d}:{minute:02d}"
            time_tuples.append(time_str)
    return tuple(time_tuples)


def now_time_interval(time_tuples):
    """ Определяет текущий АБ и выводит его в виде строки """
    now_time = datetime.now()
    now_time_time = now_time.time()
    now_time_str = now_time_time.strftime("%H:%M")
    now_ab = None  # Начальное значение переменной
    for start_time in time_tuples:
        if now_time_str >= start_time:
            now_ab = start_time
    return now_time, now_ab


def next_time_interval(time_tuples, now_ab):
    index_now_ab = time_tuples.index(now_ab)
    next_ab = None
    today_date = None
    if now_ab != "23:55":
        next_ab = time_tuples[index_now_ab + 1]
        today_date = datetime.now().date()
    else:
        next_ab = "00:00"
        # Получаем завтрашнюю дату
        today_date = datetime.now().date() + timedelta(days=1)
    next_time = datetime.combine(today_date, datetime.strptime(next_ab, "%H:%M").time())
    return next_time, next_ab


# ПРОТЕСТИРОВАНО: Эта функция корректно работает с предваряющем нулем
    # в текущем времени
# Также функция в целом работает
def where_now_ab():
    # Получаем кортеж с интервалами времени от 0:00 до 23:55
    time_tuples = generate_time_tuples()
    # Получаем текущее время и текущий АБ
    now_time, now_ab = now_time_interval(time_tuples)
    # Получаем значения начала следующего АБ и сам следующий АБ
    next_time, next_ab = next_time_interval(time_tuples, now_ab)
    delta_next_now = next_time - now_time
    delta_sec = delta_next_now.total_seconds()
    return now_ab, delta_sec


def timer_ab(target):
    """ Отдельным потоком запускает таймер, отсчитывающий АБ и выполняющий
    действие target в начале каждого ab

    target - это функция, которую должен выполнять поток в начале каждого
    """
    # TODO: Эта функция не доделана
    # Создание потока
    thread = threading.Thread(target)

    while True:
        time.sleep(where_now_ab()[1])