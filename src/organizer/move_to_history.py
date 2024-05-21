import shutil
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def move_to_history(path_to_now=r'C:\Code\orgApp Dev\resources\now',
                    path_to_history=r'C:\Code\orgApp Dev\resources\history\day'):
    """ Перемещает все файлы, которые начинаются на Day из папки now в папку
    history

    path_to_now - путь к папке now
    path_to_history - путь к папке history\day
    """
    try:
        # Проверяем существование директорий
        if not os.path.exists(path_to_now):
            logging.error(f'Папка {path_to_now} не существует.')
            return
        if not os.path.exists(path_to_history):
            logging.error(f'Папка {path_to_history} не существует.')
            return

        # Ищем все файлы, начинающиеся на 'Day' в папке now
        file_list_now = os.listdir(path_to_now)
        # Если в папке now нет файлов - выходим из функции
        if len(file_list_now) == 0:
            return
        for file in file_list_now:
            if file.startswith('Day'):
                # Формируем полный путь к файлу
                source_file = os.path.join(path_to_now, file)
                destination_file = os.path.join(path_to_history, file)

                try:
                    # Выполняем перемещение
                    shutil.move(source_file, destination_file)
                    logging.info(
                        f'Файл {file} перемещен из {path_to_now} в {path_to_history}.')
                except Exception as e:
                    logging.error(f'Ошибка при перемещении файла {file}: {e}')

    except Exception as e:
        logging.error(f'Общая ошибка: {e}')


if __name__ == "__main__":
    move_to_history()
