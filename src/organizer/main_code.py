import time
import logging
from get_name_day import get_name_day
import threading
from src.organizer.run_wb_timer import run_wb_timer
from src.organizer.run_new_wb import run_new_wb
from src.organizer.permissions.orgApp_open import open_file_app_dir_url
from src.organizer.permissions.orgApp_close import org_app_close
from src.organizer.permissions.orgApp_blocked_m import ThreadBlocked
from src.organizer.sleep_pc import sleep_pc
from src.organizer.links import *
from src.db_querys.get.get_days_from_db import get_days_from_db
from src.shared.get_today_date import get_today_date
from src.organizer.first_launch import first_launch
from src.organizer.limited_mode import LimitedMode
from src.organizer.only_schedule_mod import only_schedule_mod


def kill_new_wb(process_new_wb, blocked_obj) -> None:
    """ Ведет собственный отдельный отсчет для таймера newWB (для
    переключения между разными РБ). Записывает дынные в статистику
    выполнения, в зависимости от того, была ли нажата кнопка 'Далее'.
    При завершении таймера newWB после нажатия кнопки или при окончании
    времени его отсчета завершает текущий поток blocked

    process_new_wb (obj) - объект процесса работы таймера newWB из
    библиотеки multiprocessing.

    blocked_obj (obj) - объект потока с текущим процессом blocked.
    """

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
    # Остановка текущего blocked (по сути это blocked предыдущего РБ).
    blocked_obj.stop_flag = True


if __name__ == '__main__':

    # Запуск защитных модулей, скриптов и проверок ...
    # TODO
    # Запускаем логирование
    logging.basicConfig(filename=r'C:\Code\orgApp Dev\resources\logs\logs.log',
                        level=logging.DEBUG, filemode='a')
    logging.debug('Script started')

    #   Определить текущее название для файла Day исходя из текущей даты
    name_day = get_name_day(date='today')

    path_d_future: str = path_to_future + '\\' + name_day
    path_d_now: str = path_to_now + '\\' + name_day

    # Перемещаем старые расписания в папку history. Перемещаем расписание на сегодня из now в папку future. Функция автоматически не станет запускаться, если уже запускалась сегодня (в нее встроена проверка).
    first_launch(path_to_history=path_to_history, path_to_now=path_to_now, path_d_future=path_d_future, path_d_now=path_d_now)

    # Проверяем, нужно ли включить режим ограниченной функциональности, если да - включаем его.
    limit_mode_obj = LimitedMode()
    limit_mode_obj.get_status()
    lim_mode_status = limit_mode_obj.status
    if lim_mode_status == 'only schedule':
        # Активируем режим, когда можно только составить расписание на
        #    сегодня - больше ничего. Также с 4:00 до 5:00 будет окно,
        #    когда блокировка не будет включена.
        only_schedule_mod()

    # Получить id_days из БД табл. days на основе сегодняшней даты
    #   возвращает запись по последнему id_days на сегодня
    id_days = get_days_from_db(date=get_today_date())[0]
    
    # Устанавливаем флаги для остановки таймера
    # TODO: ? Проверить, а нужны ли они уже ?
    stop_timer: bool = False
    stop_new_wb: bool = False

    # Производим первый запуск РБ
    process_timer_rb, delta_sec, wb_title = run_wb_timer(id_days)

    # Если РБ 'sleep' - выключаем ПК
    if wb_title == 'sleep':
        sleep_pc()

    # run permissions: closed, open, blocked;
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
        dur_min_sec = '02:00'  # Время на newWB (на переключение на новый РБ)
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
                org_app_close(path_to_db, wb_title)
                open_file_app_dir_url(wb_title, path_to_db)
                # Остановка предыдущего blocked
                blocked_obj.stop_flag = True
                # Запуск нового blocked
                blocked_obj = ThreadBlocked()
                thread_blocked = threading.Thread(
                    target=blocked_obj.org_app_blocked,
                    args=(path_to_db, wb_title))
                thread_blocked.start()
