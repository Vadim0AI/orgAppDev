import pygetwindow
import psutil
from src.organizer.permissions.extract_perm import extract_perm

# TODO: Все это время можно было закрывать диспетчер задач, планировщик
#  задач, настройки времени, вместо создания двух проверяющих скриптов и
#  других функций для защиты orgApp от взлома

# TODO: Усовершенствовать функцию:
#   1. Закрытие конкретных файлов


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
    # Получаем список всех окон
    all_windows = pygetwindow.getAllTitles()

    # TODO: !!! Нужно получить разрешения в том числе на основе группы,
    #  в которой состоит РБ; См. модуль group_wb.py; Этот функционал
    #  реализовать позже - пока обойтись простым копированием разрешением и
    #  ручной их проработкой.

    # Если в начале списка dir_names: '*', то закрываем все окна,
    #   кроме последующих элементов dir_names
    if dir_names[0] == '*':
        for dir_name in dir_names:
            if all_windows.count(dir_name) > 0:
                try:
                    all_windows.remove(dir_name)
                except ValueError:
                    pass
        for window_title in all_windows:
            window = pygetwindow.getWindowsWithTitle(window_title)[0]
            window.close()
        return

    # Если в начале списка dir_names нет звездочки
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


def org_app_close(db: str, wb_title: str):
    process_names, dir_names = extract_perm(db, wb_title, type_perm='close')

    # Закрываем процессы и окна
    kill_process_by_name(process_names)
    close_window_by_title(dir_names)



if __name__ == '__main__':
    # # Список процессов для завершения
    # process_names = ["Taskmgr.exe", "mmc.exe", "SystemSettings.exe",
    #                 "vadiktxt.exe"]
    # # Список директорий / окон для закрытия (пишется title окна)
    # dir_names = ["Пользователи", "Локальный диск (C:)", "Свойства: abc",
    #                  "Разрешения для группы"]

    path_to_db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'

    org_app_close(path_to_db, 'Fun')



# TODO: Закрытие папки можно реализовать через процесс. Нужно получить
#  больше данных о процессе, например все окна, связанные с запущенным
#  процессом explorer.exe и эти окна уже закрыть
