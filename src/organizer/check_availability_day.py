import os



def check_availability_day(name_day: str,
    path_to_file = r'C:\Code\orgApp Dev\resources\now') -> bool:
    """ Проверяет наличие файла с определенным именем в указанной папке.

        Args:
        file_name (str): Имя файла, который нужно найти.
        path_to_now (str): Путь к папке, в которой нужно искать файл.

        Returns:
        bool: True, если файл существует, иначе False.
    """
    file_path = path_to_file + '\\' + name_day
    # Проверяем наличие файла
    if os.path.exists(file_path):
        return True
    else:
        return False


# Пример использования (изменить, чтобы я мог протестировать):
# file_name = "example.txt"
# folder_path = "/path/to/folder"
# if check_file_exists(file_name, folder_path):
#     print(f"Файл '{file_name}' найден в папке '{folder_path}'.")
# else:
#     print(f"Файл '{file_name}' не найден в папке '{folder_path}'.")