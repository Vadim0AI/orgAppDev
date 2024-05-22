from move_to_history import move_to_history
from check_availability_day import check_availability_day
from checking_enough_time import checking_enough_time
import shutil



def first_launch(path_to_history, path_to_now, path_to_future,
                 path_d_future, path_d_now, name_day):
    """ Перемещает старые расписания в папку history. Перемещает расписание
    на сегодня из now в папку future. Проверяет, нужно ли включить режим
    ограниченной функциональности. """

    # Переместить все файлы Day из папки now в папку history
    move_to_history(path_to_now, path_to_history)
    # Проверяем факт режима ограниченной функциональности
    #   Проверить наличие файла Day с таким названием в папке future
    file_exists = check_availability_day(name_day, path_to_future)

    #   Было ли вчера уделено достаточно времени на составление расписание на
    #       сегодня (по умолчанию - 10 мин);
    enough_time: bool = (checking_enough_time() == 10)

    # Проверяем режим ограниченной функциональности (только составление расписания)
    restriction_mode: bool = not (file_exists and enough_time)
    if restriction_mode:
        # TODO: Здесь описать действия в случае режима ограниченной
        #   функциональности
        print('Режим ограниченной функциональности')
        pass

    # Перемещаем нужный файл Day из папки future в папку now
    shutil.move(path_d_future, path_d_now)