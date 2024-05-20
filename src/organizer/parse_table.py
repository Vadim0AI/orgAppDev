import pandas as pd


def parse_table(path_to_xlsx: str) -> list:
    """ Читает xlsx файл при помощи pandas и помещает его в список python """
    # Чтение данных из xlsx-файла
    df = pd.read_excel(path_to_xlsx)
    # Замена NaN на 0
    df = df.fillna(0)
    # Преобразование данных DataFrame в список списков
    data_list = df.values.tolist()
    return data_list

path_to_xlsx = r'C:\Code\orgApp Dev\resources\templates\Day.xlsx'
table = parse_table(path_to_xlsx)
print(table)