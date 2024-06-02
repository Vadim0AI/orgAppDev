from src.organizer.permissions.extract_perm import extract_perm
from src.organizer.permissions.orgApp_close import (kill_process_by_name,
                                                    close_window_by_title)
import time


# Устанавливаем флаг остановки процесса блокировки
stop_flag = False


def org_app_blocked(db: str, wb_title: str):
    # Устанавливаем флаг остановки процесса блокировки внутри функции,
    #   чтобы при следующем запуске гарантировать, что дальнейший цикл будет
    #   запущен
    stop_flag = False

    # Получаем списки для блокировки
    process_names, dir_names = extract_perm(db, wb_title, type_perm='blocked')

    # Выполняем цикл блокировки
    while not stop_flag:
        # Закрываем процессы и окна
        kill_process_by_name(process_names)
        close_window_by_title(dir_names)
        time.sleep(1)
