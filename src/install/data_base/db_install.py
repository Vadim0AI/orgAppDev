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
                  enough_time INTEGER)''')

# Создаем таблицу wb (таблица с РБ и разрешениями к ним)
cursor.execute('''CREATE TABLE IF NOT EXISTS wb
                  (title TEXT PRIMARY KEY, 
                  open TEXT, 
                  close TEXT,
                  blocked TEXT)''')

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

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()
