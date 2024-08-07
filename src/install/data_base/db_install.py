import sqlite3


# Устанавливаем соединение с базой данных
#   (если такой базы данных нет, она будет автоматически создана)
conn = sqlite3.connect(r'C:\Code\orgApp Dev\resources\db\orgApp.db')

# Создаем курсор для работы с базой данных
cursor = conn.cursor()

# Создаем таблицу days (таблица с расписаниями в целом)
cursor.execute('''CREATE TABLE IF NOT EXISTS days
                  (id_days INTEGER PRIMARY KEY, 
                  date INTEGER, 
                  version INTEGER,  
                  time_change INTEGER,
                  limited_status TEXT,
                  first_launch INTEGER)''')

# таблица days (описание):
# id_days INTEGER PRIMARY KEY,
# date INTEGER,
# version INTEGER - от 1 до беск.
# time_change INTEGER - время внесения нового расписания в таблицу,
#   в формате '%H:%M:%S %d.%m.%y'
# limited_status TEXT - статус режима ограниченной функциональности:
    # 1. 'indefinite' - неопределенное значение;
    # 2. 'only schedule' - расписания на сегодня нет - можно только составлять расписание;
    # 3. 'no leisure' - расписание не было составлено заранее на сегодня, его составили сегодня же. Поэтому запрещено добавлять развлекательные РБ и другие подобные.
    # 4. 'no limited' - никаких ограничений на добавление РБ. Расписание на сегодня было составлено заранее, как минимуум еще вчера.
# first_launch INTEGER:
    # 0 - функция first_launch еше не была выполнена ни разу за день;
    # 1 - была выполнена функция first_launch, которая перемещает файлы в папки history из now, и в now из tomorrow, а также проверяет есть ли сейчас режим ограниченной функциональности (но при этом сам статус наличия этого режима здесь не отображается).
    
# Создаем таблицу wb (таблица с РБ и разрешениями к ним)
cursor.execute('''CREATE TABLE IF NOT EXISTS wb
                  (id INTEGER PRIMARY KEY,
                  wb_group TEXT,
                  title TEXT,
                  open TEXT, 
                  close TEXT,
                  blocked TEXT,
                  settings TEXT)''')

# таблица wb (описание):
# ...
# settings TEXT - для указания настроек для РБ. Формат такой:
# 'тип_настройки_1 : значение_1, значение_2 | тип_настройки_2 : ...'
# разделитель между типами настроек ' | '
# Между типом настройки и значениями ' : '
# Между настройками в рамках одного типа ', '

# поле для указания того, можно ли сдвигать этот РБ в
# расписании и тип разрешенного сдвига. Например: 'all' - можно двигать как
# угодно. 'right' - можно сдвигать только вперед во времени.
# duration TEXT - можно ли увеличивать / уменьшать длительность РБ в текущем
# расписании. 'all' - можно как угодно. 'reduce' - общую длительность на
# день можно только уменьшать.

# Создаем таблицу day_wb (таблица с расписанием по РБ)
cursor.execute('''CREATE TABLE IF NOT EXISTS day_wb
                  (id_days INTEGER, 
                  number INTEGER, 
                  wb_start TEXT, 
                  wb_title TEXT, 
                  fact INTEGER, 
                  fix INTEGER, 
                  duration TEXT, 
                  FOREIGN KEY (id_days) REFERENCES days (id_days), 
                  FOREIGN KEY (wb_title) REFERENCES wb (title))''')

# Создаем таблицу setting (таблица с настройками orgApp)
# TODO: Реализовать в версии v2
# cursor.execute('''CREATE TABLE IF NOT EXISTS setting
# ''')

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()
