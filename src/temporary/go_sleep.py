import time

import psutil
import pygetwindow
import os
import datetime


def kill_process_by_name(process_names):
    """Завершает процесс по его имени."""
    for process_name in process_names:
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                proc.kill()
                print(f"Процесс {process_name} завершен.")
                return
        print(f"Процесс {process_name} не найден.")

def close_window_by_title(dir_names):
    """ Закрывает окна Windows по их title """
    all_windows = pygetwindow.getAllTitles()
    print(all_windows)
    for dir_name in dir_names:
        # Проверяем каждое окно на полное совпадение с заголовком
        for window_title in all_windows:
            if dir_name == window_title:
                # Если найдено полное совпадение, закрываем окно и завершаем функцию
                window = pygetwindow.getWindowsWithTitle(window_title)[0]
                window.close()
                return
        # Если не найдено полного совпадения, выводим сообщение об ошибке
        print(f"Окно с заголовком '{dir_name}' не найдено.")


# Функция для выключения компьютера
def shutdown_computer():
    os.system("shutdown /s /t 1")




if __name__ == '__main__':

    # Получаем текущее время
    current_time = datetime.datetime.now().time()

    while True:

        # Проверяем, находится ли текущее время в интервале с 22:00 до 3:00
        if (datetime.time(22, 0,
                          0) <= current_time <= datetime.time(23,
                                                              59,
                                                              59)) or \
                (datetime.time(0, 0,
                               0) <= current_time <= datetime.time(
                    3, 0, 0)):
            # shutdown_computer()
            print("Компьютер выключается...")
        else:
            print("Текущее время не в интервале с 22:00 до 3:00.")



        # Проверяем, находится ли текущее время в интервале с 4:00 до 8:00
        if (datetime.time(4, 0,
                          0) <= current_time <= datetime.time(8,
                                                              0,
                                                              0)):
            print("Текущее время находится в интервале с 4:00 до 8:00.")
            pass
        else:
            print("Текущее время не находится в интервале с 4:00 до 8:00.")
            # Список директорий / окон для закрытия (пишется title окна)
            dir_names = ['Изменить дату и время']
            close_window_by_title(dir_names)
            # Список процессов для завершения
            process_names = ['Taskmgr.exe', 'mmc.exe', 'firefox.exe']
            kill_process_by_name(process_names)

        time.sleep(1)