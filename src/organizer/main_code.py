from src.organizer.interface.wb_timer import CountdownTimer
from parse_table import parse_table
from where_now_ab import where_now_ab
from move_to_history import move_to_history
from get_name_day import get_name_day
from check_availability_day import check_availability_day
from checking_enough_time import checking_enough_time
from where_now_wb import where_now_wb
import threading
from src.organizer.interface.wb_timer import CountdownTimer
from src.organizer.interface.new_wb import NewWB
import shutil
from first_launch import first_launch
from loading_schedule import loading_schedule



# Запуск защитных модулей, скриптов и проверок ...

# TODO: Сделать отдельный файл для всех зависимостей
path_to_now = r'C:\Code\orgApp Dev\resources\now'
path_to_history = r'C:\Code\orgApp Dev\resources\history\day'
path_to_future = r'C:\Code\orgApp Dev\resources\future'
db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'

#   Определить текущее название для файла Day исходя из текущей даты
name_day = get_name_day(date='today')

path_d_future: str = path_to_future + '\\' + name_day
path_d_now: str = path_to_now + '\\' + name_day

# Перемещаем старые расписания в папку history. Перемещаем расписание
#     на сегодня из now в папку future. Проверяем, нужно ли включить режим
#     ограниченной функциональности.
# first_launch(path_to_history, path_to_now, path_to_future, path_d_future,
#              path_d_now, name_day)

# TODO: Нужно сначала получить этот id_days на основе последнего
#  существующего id_days
# TODO: В случае первой записи расписания на день, нужно также добавлять
#  строку в таблицу базы данных "days". id_days, date, version, time_change
id_days = 1

loading_schedule(db, id_days, path_d_now)





# Запускаем цикл РБ ...
while True:
    # Произвожу поиск текущего РБ в таблице БД "day_wb",
    #   отсеивая по id_days ...
    now_wb = where_now_wb(id_days)
    print(now_wb)
    if now_wb == 'sleep':
        pass # TODO: дописать - что делать, если время sleep ...
    wb_row, delta_sec = now_wb

    #   Для этого нужно получить: длительность РБ
    # Запускаю таймер РБ

    duration_min = int(delta_sec / 60)
    duration_sec = delta_sec - (duration_min * 60)
    # длительность РБ в формате 'mm:ss'
    dur_min_sec: str = '{:02d}:{:02d}'.format(duration_min, duration_sec)
    # Чтобы запустить таймер, нужно получить общее время для отсчета и title
    #   задачи РБ
    wb_title = wb_row[3]
    # Определяем объект таймера и запускаем его в отдельном потоке
    timer_app = CountdownTimer(dur_min_sec, wb_title)
    timer_thread = threading.Thread(target=timer_app.mainloop())
    timer_thread.start()

    # После завершения таймера - окно подтверждения окончания РБ ...
    # Дописать меню для orgApp ...
    # Выключение ПК в случае РБ "sleep"
    # Запускаю open, close, blocked


# При запуске изменения текущего расписания или составления расписания на
#   завтра, вне соответствующего РБ, создается и запускается нужный РБ.

# Функционал при нажатии "скорректировать текущее расписание" ...
#   ...

# Функционал при нажатии "расписание на завтра / edit" ...
#   ...

# Интерфейс:
# Функция добавления и корректировки плана на завтра ...
