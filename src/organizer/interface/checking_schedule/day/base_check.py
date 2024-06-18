import openpyxl


def base_check(template_path, day_path, sheet_name):
    # Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    #   этого обращаемся к детализированным версиям расписаний;
    if not num_rows_check(template_path, day_path, sheet_name):
        return False


    # Парсим таблицу с расписанием в список / кортеж
    #   (получаем расписание по РБ);
    # Первый блок - 'start day' и он не раньше 4:00
    # Последний блок - 'sleep' и он не позднее 23:00
    # Проверяем, что нет пустых РБ между началом и концом расписания;
    # Проверяем, что все РБ расписания есть в БД;
    # Проверка: кол-во РБ в расписании не менее пяти;
    # В расписании должен быть РБ "plan day", длительностью не менее десяти
    #   минут;
    return True


def num_rows_xlsx(path_to_xlsx, sheet_name):
    """ Отрывает excel и считает кол-во строк, в которых есть хотя бы одно
    значение """
    # Открываем Excel-файл с помощью with
    with openpyxl.load_workbook(path_to_xlsx) as workbook:
        # Получаем лист по имени
        sheet = workbook[sheet_name]
        # Получаем количество заполненных строк
        last_row = sheet.max_row
        return last_row
    # Файл автоматически закрывается после выполнения блока with


def num_rows_check(template_path, day_path, sheet_name):
    """ Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    этого обращаемся к детализированным версиям расписаний """
    num_rows_temp = num_rows_xlsx(template_path, sheet_name)
    num_rows_day = num_rows_xlsx(day_path, sheet_name)
    if num_rows_temp == num_rows_day:
        return True
    else:
        return False








