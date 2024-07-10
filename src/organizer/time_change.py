import os
import time


def watch_folder(folder_path):
    # Получаем время последнего изменения папки
    last_modified_time = os.path.getmtime(folder_path)

    while True:
        # Проверяем время последнего изменения
        current_modified_time = os.path.getmtime(folder_path)
        if current_modified_time != last_modified_time:
            print("Папка была изменена или удалена!")
            return True

        # Ждем 1 секунду перед следующей проверкой
        time.sleep(1)


# Укажите путь к папке, которую вы хотите отслеживать
folder_path = r'C:\Users\AI\Desktop\abc'

# Запускаем функцию отслеживания папки
watch_folder(folder_path)
