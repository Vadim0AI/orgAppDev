from src.organizer.permissions.extract_perm import extract_perm
from src.organizer.permissions.orgApp_close import (kill_process_by_name,
                                                    close_window_by_title)
import time

class ThreadBlocked():
    def __init__(self):
        self.stop_flag = False

    def org_app_blocked(self, db: str, wb_title: str):
        # Устанавливаем флаг остановки процесса блокировки внутри функции,
        #   чтобы при следующем запуске гарантировать, что дальнейший цикл будет
        #   запущен
        self.stop_flag = False

        # Получаем списки для блокировки
        process_names, dir_names = extract_perm(db, wb_title,
                                                type_perm='blocked')

        # Выполняем цикл блокировки
        while not self.stop_flag:
            # Закрываем процессы и окна
            kill_process_by_name(process_names)
            close_window_by_title(dir_names)
            time.sleep(1)
