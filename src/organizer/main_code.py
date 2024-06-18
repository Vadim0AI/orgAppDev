import time
from get_name_day import get_name_day
import threading
from check_availability_day import check_availability_day
from first_launch import first_launch
from loading_schedule import loading_schedule
from src.organizer.run_wb_timer import run_wb_timer
from src.organizer.run_new_wb import run_new_wb
from src.organizer.permissions.orgApp_open import open_file_app_dir_url
from src.organizer.permissions.orgApp_close import org_app_close
from src.organizer.permissions.orgApp_blocked_m import ThreadBlocked
from src.organizer.sleep_pc import sleep_pc


def kill_new_wb(process_new_wb, wb_title, path_to_db):
    time_to_newWB = 120
    global stop_flag
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

    # TODO: Сделать отдельный файл для всех зависимостей (есть модуль links,
    #  но нужно реализовать безошибочную подгрузку из него позже)
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
    # TODO: Реализовать запись в соответсвующую таблицу БД (статус
    #  ограниченной функциональности на день, факт first_launch за этот день)
    # first_launch(path_to_history, path_to_now, path_to_future, path_d_future,
    #              path_d_now, name_day)

    # TODO: Нужно сначала получить этот id_days на основе последнего
    #  существующего id_days
    # TODO: В случае первой записи расписания на день, нужно также добавлять
    #  строку в таблицу базы данных "days". id_days, date, version, time_change
    id_days = 1

    # Парсим расписание на день из excel и помещает в БД.
    # TODO: Возможно это не потребуется т.к. это происходит через кнопки
    #  интерфейса, просто нужно сдлеать правильное переключение на нужный
    #  день. Т.е. при составлении на завтра, все парсится в БД, а от туда
    #  уже используется
    # loading_schedule(path_to_db, id_days, path_d_now)

    stop_timer = False
    stop_new_wb = False

    # Производим первый запуск РБ
    process_timer_rb, delta_sec, wb_title = run_wb_timer(id_days)

    # Если РБ 'sleep' - выключаем ПК
    if wb_title == 'sleep':
        sleep_pc()

    # run permissions: closed, open, blocked;
    # TODO: Похоже closed, open, blocked используют значения не из БД,
    #  а из excel напрямую - исправить !!!
    org_app_close(path_to_db, wb_title)
    open_file_app_dir_url(wb_title, path_to_db)

    # Запуск потока для blocked
    blocked_obj = ThreadBlocked()
    thread_blocked = threading.Thread(target=blocked_obj.org_app_blocked,
                                      args=(path_to_db, wb_title))
    thread_blocked.start()

    # Ждем, пока не закончится РБ
    time.sleep(delta_sec)

    # TODO: Нужно остановить ранее запущенный поток blocked;

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
        # Ожидание newWB (время на нажатие кнопки Next). sleep_new_wb
        #   отслеживает завершение процесса таймера new_wb, и в зависимости от
        #   того, была ли нажата кнопка Next, или время было упущено -
        #   вносит данные в статистику, а также выполняет closed, open,
        #   blocked;
        thread_sleep_new_wb = threading.Thread(target=kill_new_wb,
                                               args=(process_new_wb,
                                                     blocked_obj))
        thread_sleep_new_wb.start()

        # Флаг, обозначающий, было ли выполнено: closed, open, blocked;
        permissions_run = False

        # Ждем окончания РБ
        while delta_sec >= 0:
            delta_sec -= 1
            time.sleep(1)

            # Выполняем проверку - жив ли процесс таймера new_wb, если нет -
            #   closed, open, blocked
            if not process_new_wb.is_alive() and not permissions_run:
                permissions_run = True
                # Если РБ 'sleep' - выключаем ПК
                if wb_title == 'sleep':
                    sleep_pc()
                # run permissions: closed, open;
                open_file_app_dir_url(wb_title, path_to_db)
                org_app_close(path_to_db, wb_title)
                # Остановка предыдущего blocked
                blocked_obj.stop_flag = True
                # Запуск нового blocked
                blocked_obj = ThreadBlocked()
                thread_blocked = threading.Thread(
                    target=blocked_obj.org_app_blocked,
                    args=(path_to_db, wb_title))
                thread_blocked.start()


        # Дописать меню для orgApp ...


        # При запуске изменения текущего расписания или составления расписания
        # на завтра, вне соответствующего РБ, создается и запускается нужный
        # РБ.

        # Функционал при нажатии "скорректировать текущее расписание" ...
        #   ...

        # Функционал при нажатии "расписание на завтра / edit" ...
        #   ...

        # Интерфейс:
        # Функция добавления и корректировки плана на завтра ...
