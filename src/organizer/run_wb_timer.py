import multiprocessing
from src.db_querys.get.where_now_wb import where_now_wb
from src.organizer.interface.wb_timer import run_wb
from src.organizer.sleep_pc import sleep_pc


def run_wb_timer(id_days):
    # Произвожу поиск текущего РБ в таблице БД "day_wb",
    #   отсеивая по id_days ...
    now_wb = where_now_wb(id_days)
    if now_wb == 'sleep':
        sleep_pc()
    wb_row, delta_sec = now_wb

    #   Для этого длительность РБ
    duration_min = int(delta_sec / 60)
    duration_sec = delta_sec - (duration_min * 60)
    # длительность РБ в формате 'mm:ss'
    dur_min_sec: str = '{:02d}:{:02d}'.format(duration_min, duration_sec)
    # Получаем title
    wb_title = wb_row[3]

    # Запускаем таймер РБ в новом процессе
    process_timer_rb = multiprocessing.Process(target=run_wb,
                                               args=(dur_min_sec, wb_title))
    process_timer_rb.start()

    return process_timer_rb, delta_sec, wb_title
