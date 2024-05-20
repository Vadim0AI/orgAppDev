from src.organizer.kivi_interface.wb_timer import CountdownTimer
from parse_table import parse_table
from day_ab_to_wb import day_wb_in_db
from where_now_ab import where_now_ab
from move_to_history import move_to_history
from get_name_day import get_name_day
from check_availability_day import check_availability_day
from checking_enough_time import checking_enough_time
from where_now_wb import where_now_wb
import threading


# Запуск защитных модулей, скриптов и проверок ...

# TODO: Сделать отдельный файл для всех зависимостей
path_to_now = r'C:\Code\orgApp Dev\resources\now'
path_to_history = r'C:\Code\orgApp Dev\resources\history\day'
path_to_future = r'C:\Code\orgApp Dev\resources\future'

# --- При запуске orgApp --- :
# Переместить все файлы Day из папки now в папку history
move_to_history(path_to_now, path_to_history)

# Проверяем факт режима ограниченной функциональности
#   Определить текущее название для файла Day исходя из текущей даты
name_day = get_name_day(date='today')
# Проверить наличие файла Day с таким названием в папке future
file_exists = check_availability_day(name_day, path_to_future)

#   Было ли вчера уделено достаточно времени на составление расписание на
#       сегодня (по умолчанию - 10 мин);
enough_time: bool = (checking_enough_time() == 10)

# Проверяем режим ограниченной функциональности (только составления расписания)
restriction_mode: bool = not (file_exists and enough_time)
if restriction_mode:
    # TODO: Здесь описать действия в случае режима ограниченной
    #   функциональности
    pass

# Парсим расписание на день
db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
path_day = r'C:\Code\orgApp Dev\resources\now\Day.xlsx'
# TODO: Нужно сначала получить этот id_days на основе последнего
#  существующего id_days
id_days = 1
day_ab = parse_table(path_day)
print(day_ab)
# Трансформируем список с расписанием по АБ в формат РБ и помещаем его в
#   таблицу БД "day_wb"
day_wb_in_db(db, id_days, day_ab)
# TODO: В случае первой записи расписания на день, нужно также добавлять
#  строку в таблицу базы данных "days". id_days, date, version, time_change

# Запускаем цикл РБ ...
while True:
    # Произвожу поиск текущего РБ в таблице БД "day_wb",
    #   отсеивая по id_days ...
    now_wb = where_now_wb(id_days)
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
    timer_thread = threading.Thread(target=timer_app.run())
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
