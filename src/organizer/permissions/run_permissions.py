from src.db_querys.set.parse_wb import parse_wb

# РБ выстраиваются в иерархию наследования. Наибольший приоритет
#   разрешений имеет сам РБ, затем его РБ. Это позволяет излишне не писать в
#   каждом РБ одни и те же разрешения.

# 0. Парсим таблицу в БД при наличии определенного действия





# 1. Из БД парсим подходящий РБ и его группу (в том числе
# группу группы), с учетом его группы получаем разрешения;
# Возвращаем:
#   close (1) Список процессов для завершения; (2) Список директорий
#       / окон для закрытия (пишется title окна);
#   open: URL или путь к файлу / директории для открытия (все в одном списке
#   - функция сама определит что это)

# 2. Выполняем close, open
# 3. Запускаем цикл blocked

if __name__ == '__main__':
    path_to_wb = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'
    path_to_db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
    parse_wb(path_to_db, path_to_wb)
