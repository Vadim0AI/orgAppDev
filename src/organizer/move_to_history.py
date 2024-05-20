import shutil
import os



def move_to_history(path_to_now=r'C:\Code\orgApp Dev\resources\now',
                    path_to_history=r'C:\Code\orgApp Dev\resources\history\day'):
    """ Перемещает все файлы, которые начинаются на Day из папки now в папку
    history

    path_to_now - путь к паке now
    path_to_history - путь к папке history\day
    """
    # 1. Ищем все файлы Day в папке now
    file_list_now = os.listdir(path_to_now)
    for file in file_list_now:
        if file.startswith('Day'):
            # 2. Выполняем перемещение
            shutil.move(file, path_to_history)