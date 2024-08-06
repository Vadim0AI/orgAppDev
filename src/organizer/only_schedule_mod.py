import datetime
import time

from src.organizer.sleep_pc import sleep_pc
from src.organizer.interface.wb_timer import CountdownTimer
import threading
from src.organizer.permissions.orgApp_blocked_m import ThreadBlocked
from src.organizer.links import path_to_db


def only_schedule_mod():
    # 1. Проверить текущее время - если сейчас время выключения или позже до
    #   4 утра (sleep по умолчанию с 23:00) - выключить ПК. Начать вести
    #   отсчет до sleep.
    # 2. Запустить таймер РБ c title "schedule for today" и
    #   длительностью от текущего времени, до времени sleep по умолчанию.
    # 3. Выполнять первый раз действие таймера РБ wb_timer.today_action() -
    #   это откроет таблицу с расписанием на сегодня.
    # 4. Запустить поток blocked, запрещающий все, кроме составления
    #   расписания на сегодня.
    # 5. Если расписание не было составлено, то ПК выключается при окончании
    # отсчета до sleep.
    # После нажатия на кнопку 'Today' на таймере, если расписание успешно
    # прошло проверку, будет выведено соответсвующее уведомление и ПК будет
    # перезагружен.
    # После этого запустится main_code.py в нем будет проверка
    # limit_mode_obj.get_status() т.к. расписание на сегодня уже появилось,
    #   то он даст статус 'no leisure'.

    # TODO: Нужно сделать окно для корректировки orgApp, когда ограничения
    #  не работают. Например, с 4:00 до 5:00. Однако, нужно не забыть
    #  включить эти ограничения, как только окно закончится.

    # -- Проверяем - нужно ли выключить ПК из-за sleep по умолчанию ---
    # Получение текущего времени
    now = datetime.datetime.now()
    # Создание объекта datetime.time с часами и минутами из текущего времени
    current_time = datetime.time(now.hour, now.minute)
    # Определение начала и конца интервала
    start_time = datetime.time(4, 0)  # 4:00
    window_end_time = datetime.time(5, 0)  # 5:00
    end_time = datetime.time(23, 0)  # 23:00
    # Проверка, что текущее время находится в заданном интервале
    if start_time <= current_time <= end_time:
        pass # Все в порядке - ничего не делаем
    else:
        # Текущее время НЕ находится в интервале от 4:00 до 23:00
        #   - выключить ПК.
        sleep_pc()

    # --- Начинаем вести отсчет до выключения ПК из-за sleep по умолчанию ---
    # Преобразование текущего времени и времени 23:00 в объекты datetime
    #   с текущей датой.
    current_datetime = datetime.datetime.combine(now.date(), current_time)
    end_datetime = datetime.datetime.combine(now.date(), end_time)
    # Вычисление разницы между текущим временем и временем 23:00
    time_difference = end_datetime - current_datetime
    # Получение разницы в минутах и секундах
    minutes, seconds = divmod(time_difference.seconds, 60)
    # Время до выключения ПК в секундах.
    dur_to_end_day = (minutes * 60) + seconds
    # В отдельном потоке отсчет времени до выключения ПК, там же и
    # срабатывает выключение по окончании времени.
    countdowning_thread = threading.Thread(target=countdowning, args=(
        dur_to_end_day,))
    countdowning_thread.start()

    # --- Запускаем интерфейс таймера ---
    obj_timer = CountdownTimer(time_remaining=f'{minutes}:{seconds}',
                             description='schedule for today')
    # Создаем и открываем пустое расписание на сегодня.
    obj_timer.today_action()
    # Запускаем таймер РБ
    obj_timer.mainloop()


    while True:
        time.sleep(1)


def countdowning(dur_to_end_day):
    """ Ведет обратный отсчет времени до конца дня (sleep по умолчанию).
    Включает блокировку, если текущее время вне окна с 4:00 до 5:00 """

    # Создаем поток для blocked, но пока не запускаем
    # !!! В таблице wb обязательно должен быть РБ 'only schedule mod' -
    # именно этот РБ отвечает, за то, что будет блокироваться в этом режиме.
    blocked_obj = ThreadBlocked()
    thread_blocked = threading.Thread(target=blocked_obj.org_app_blocked,
                                      args=(path_to_db, 'only schedule mod'))

    # С 4:0 до 5:00 - окно когда блокировка работать не будет.
    start_time = datetime.time(4, 0)  # 4:00
    window_end_time = datetime.time(5, 0)  # 5:00

    blocked_activate = False

    while dur_to_end_day > 0:
        dur_to_end_day -= 1
        time.sleep(1)
        if blocked_activate == False:
            # Получение текущего времени
            now = datetime.datetime.now()
            current_time = now.time()
            # Если текущее время вне окна для изменения orgApp (с 4:00 до 5:00) и
            # при этом блокировка ранее не была запущена - запускаем блокировку.
            if not (start_time <= current_time <= window_end_time) and (
                    blocked_activate == False):
                thread_blocked.start()
                blocked_activate = True
    else:
        # Как только обратный отсчет закончен - выключаем ПК.
        sleep_pc()
