import time
import multiprocessing
from parse_table import parse_table
from get_name_day import get_name_day
from where_now_wb import where_now_wb
import threading
from src.organizer.interface.wb_timer import run_wb
from src.organizer.interface.new_wb import NewWB
from first_launch import first_launch
from loading_schedule import loading_schedule
from src.organizer.run_wb_timer import run_wb_timer
from src.organizer.run_new_wb import run_new_wb


# TODO: !!! При запуске таймера, он вычисляет время без учета секунд,
#  получается некорректный ход таймера. Он всегда запускает минуты ровно.
#   Как я выяснил - ошибка где-то в where_now_wb. Также из-за этого
#   неправильного подсчета, он при переходе между РБ считает delta_sec
#   равным 1 секунде

def sleep_new_wb(process_new_wb):
    time_to_newWB = 120
    while process_new_wb.is_alive():
        if time_to_newWB <= 0:
            process_new_wb.kill()
            # TODO: Записать в БД и в таблицу Day, что РБ НЕ был выполнен;
        time.sleep(1)
        time_to_newWB -= 1
    else:
        # TODO: Записать в БД и в таблицу Day, что РБ БЫЛ выполнен (если
        #  была нажата кнопка Next);
        pass


if __name__ == '__main__':

    # Запуск защитных модулей, скриптов и проверок ...

    # TODO: Сделать отдельный файл для всех зависимостей
    path_to_now = r'C:\Code\orgApp Dev\resources\now'
    path_to_history = r'C:\Code\orgApp Dev\resources\history\day'
    path_to_future = r'C:\Code\orgApp Dev\resources\future'
    path_to_db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
    path_to_wb = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'

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

    # Парсим расписание на день из excel и помещает в БД.
    # loading_schedule(path_to_db, id_days, path_d_now)

    stop_timer = False
    stop_new_wb = False

    # Производим первый запуск РБ
    process_timer_rb, delta_sec, wb_title = run_wb_timer(id_days)
    # Ждем, пока не закончится РБ
    time.sleep(delta_sec)

    # TODO: run permissions: closed, open, blocked;

    # Запускаем цикл РБ
    while True:

        # Если таймер РБ еще не закончился - завершаем его процесс
        while process_timer_rb.is_alive():
            process_timer_rb.kill()
            time.sleep(2)

        # Запускаем таймер new РБ
        dur_min_sec = '02:00'  # Время на newWB
        process_new_wb = run_new_wb(dur_min_sec, wb_title)
        # Запускаем таймер следующего РБ
        process_timer_rb, delta_sec, wb_title = run_wb_timer(id_days)
        # Ожидание newWB (время на нажатие кнопки Next). Если кнопка не
        #   нажата, то срабатывает действие
        thread_sleep_new_wb = threading.Thread(target=sleep_new_wb,
                                               args=(process_new_wb,))
        thread_sleep_new_wb.start()
        # run permissions: closed, open, blocked;


        # Ждем окончания РБ
        if process_timer_rb.is_alive():
            time.sleep(delta_sec)




        # После завершения таймера - окно подтверждения окончания РБ ...
        # Дописать меню для orgApp ...
        # Выключение ПК в случае РБ "sleep"
        # Запускаю open, close, blocked


        # При запуске изменения текущего расписания или составления расписания
        # на завтра, вне соответствующего РБ, создается и запускается нужный
        # РБ.

        # Функционал при нажатии "скорректировать текущее расписание" ...
        #   ...

        # Функционал при нажатии "расписание на завтра / edit" ...
        #   ...

        # Интерфейс:
        # Функция добавления и корректировки плана на завтра ...
