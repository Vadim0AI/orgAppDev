from src.shared.xlsx_utils.num_rows_xlsx import num_rows_xlsx


def base_check(template_path, day_path, sheet_name):
    # TODO: [~] base_check()
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


def num_rows_check(template_path, day_path, sheet_name):
    """ Проверяем кол-во строк в файле (должно совпадать с шаблоном) - для
    этого обращаемся к детализированным версиям расписаний """
    num_rows_temp = num_rows_xlsx(template_path, sheet_name)
    num_rows_day = num_rows_xlsx(day_path, sheet_name)
    if num_rows_temp == num_rows_day:
        return True
    else:
        return False








