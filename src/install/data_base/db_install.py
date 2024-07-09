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
                  enough_time INTEGER,
                  first_load INTEGER)''')

# таблица days (описание):
# id_days INTEGER PRIMARY KEY,
# date INTEGER,
# version INTEGER - от 1 до беск.
# time_change INTEGER - время внесения нового расписания в таблицу,
#   в формате '%H:%M:%S %d.%m.%y'
# enough_time INTEGER,
# first_load INTEGER

# Создаем таблицу wb (таблица с РБ и разрешениями к ним)
cursor.execute('''CREATE TABLE IF NOT EXISTS wb
                  (id INTEGER PRIMARY KEY,
                  wb_group TEXT,
                  title TEXT,
                  open TEXT, 
                  close TEXT,
                  blocked TEXT,
                  shift TEXT,
                  duration TEXT)''')

# таблица wb (описание):
# ...
# shift TEXT - поле для указания того, можно ли сдвигать этот РБ в
# расписании и тип разрешенного сдвига. Например: 'all' - можно двигать как
# угодно. 'right' - можно сдвигать только вперед во времени.
# duration TEXT - можно ли увеличивать / уменьшать длительность РБ в текущем
# расписании. 'all' - можно как угодно. 'reduce' - общую длительность на
# день можно только уменьшать.

# Создаем таблицу day_wb (таблица с расписанием по РБ)
cursor.execute('''CREATE TABLE IF NOT EXISTS day_wb
                  (id_days INTEGER, 
                  number INTEGER, 
                  wb TEXT, 
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
