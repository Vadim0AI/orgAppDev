import openpyxl


def num_rows_xlsx(path_to_xlsx, sheet_name):
    """
    Функция, которая открывает Excel-файл, находит указанный лист и
    возвращает количество заполненных строк в этом листе.

    Параметры:
    path_to_xlsx (str): Путь к Excel-файлу.
    sheet_name (str): Название листа, для которого нужно посчитать
                      количество заполненных строк.

    Возвращает:
    int: Количество заполненных строк в указанном листе.
    """
    # Открываем Excel-файл
    workbook = openpyxl.load_workbook(path_to_xlsx)

    # Получаем лист по имени
    sheet = workbook[sheet_name]

    # Получаем количество заполненных строк
    last_row = sheet.max_row

    # Закрываем рабочую книгу
    workbook.close()

    # Возвращаем количество заполненных строк
    return last_row
