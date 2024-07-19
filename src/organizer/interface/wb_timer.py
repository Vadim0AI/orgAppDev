import tkinter as tk
import win32gui
import win32con
import os
from src.organizer.interface.is_excel_file_open import is_excel_file_open
from src.organizer.get_open_windows_with_processes import get_open_windows_with_processes
from plyer import notification
from src.db_querys.get.wb_in_excel import wb_db_in_excel
from src.db_querys.set.parse_wb import parse_wb
from src.organizer.get_name_day import get_name_day
from src.organizer.links import (path_to_future, path_to_clean_templates,
                                 path_to_db, path_day_temp, path_to_now)
import shutil
# from src.organizer.loading_schedule import loading_schedule
from src.db_querys.set.add_day_schedule import add_day_schedule
from win10toast import ToastNotifier
from datetime import datetime, timedelta
from src.organizer.checking_schedule.day.base_check import base_check
from src.organizer.checking_schedule.day.dur_shift_check import dur_shift_check
from src.shared.xlsx_utils.parse_table import parse_table
from src.db_querys.get.extract_db import extract_db
from src.db_querys.get.get_days_from_db import get_days_from_db



class CountdownTimer(tk.Tk):
    """
        Таймер для отсчета РБ

        Класс NewWB представляет собой окно, созданное с использованием
            Tkinter, которое отображает
        таймер обратного отсчета и описание задачи. Окно может быть
            зафиксировано сверху других окон
        и имеет функциональность для отображения дополнительных кнопок меню
            при нажатии кнопки "Menu".

        Атрибуты:
        - time_remaining (int): Время, оставшееся до завершения таймера,
            в секундах.
        - description (str): Обрезанное до 25 символов описание задачи.
        - is_fixed (bool): Флаг, указывающий, зафиксировано ли окно сверху
            других окон.
        - hwnd (int or None): Дескриптор окна для взаимодействия с Win32 API.
        - menu_buttons_visible (bool): Флаг, указывающий, отображены ли
            дополнительные кнопки меню.
        - menu_buttons_height (int): Высота дополнительных кнопок меню
            в пикселях.

        Методы:
        - __init__(self, time_remaining, description, *args, **kwargs):
            Инициализирует окно, устанавливает начальные значения атрибутов,
            создает основные виджеты и запускает таймер.
        - set_window_position(self): Устанавливает начальное положение окна и
            фиксирует его сверху.
        - update_timer(self): Обновляет таймер каждую секунду и завершает его
            при достижении нуля.
        - update_action(self): Обрабатывает нажатие кнопки "Today"
            (в данный момент просто печатает сообщение).
        - menu_action(self, action=None): Обрабатывает нажатие кнопки "Menu",
            отображает или скрывает дополнительные кнопки меню и корректирует положение окна.
        - activate_window(self): Активирует окно, переводя его на передний план.
        - fix_action(self): Фиксирует или освобождает окно сверху других окон,
            в зависимости от текущего состояния.
        - set_always_on_top(self): Устанавливает окно поверх всех других окон.
        - unset_always_on_top(self): Снимает окно с фиксированного верхнего
            положения.
        - parse_time(time_str): Преобразует строковое представление времени в
            секунды.
        - format_time(seconds): Форматирует время в секунды в строку формата
            "мм:сс".
        - trim_description(description): Обрезает описание задачи до 25 символов.
        - play_sound(self): Воспроизводит звуковое уведомление
            (в данный момент метод не используется).
        - stop(self): Останавливает таймер и закрывает окно.

        Использование:
        Пример создания экземпляра окна с таймером на 1 минуту и 10 секунд и описанием задачи:
            app = NewWB('01:10', 'Описание задачи')
            app.mainloop()
        """


    def __init__(self, time_remaining, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_remaining = self.parse_time(time_remaining)
        self.description = self.trim_description(description)
        self.is_fixed = False
        self.hwnd = None
        self.title("CountdownTimer")
        self.geometry("180x40+1354+792")
        self.configure(bg='#252824')
        self.overrideredirect(True)

        self.label = tk.Label(self, text="     " + self.format_time(self.time_remaining) + "  |  " + self.description,
                              bg='#252824', fg='white', anchor='w')
        self.label.pack(fill=tk.BOTH, expand=True)

        button_frame_1 = tk.Frame(self, bg='#252824')
        button_frame_1.pack(fill=tk.X)

        self.menu_button = tk.Button(button_frame_1, text="Menu",
                                     bg='#252824', fg='white', command=self.menu_action)
        self.menu_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.today_button = tk.Button(button_frame_1, text="Today",
                                      bg='#252824', fg='white',
                                      command=self.today_action)
        self.today_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.today_button = tk.Button(button_frame_1, text="Temp.",
                                      bg='#252824', fg='white',
                                      command=self.temp_action)
        self.today_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.fix_button = tk.Button(button_frame_1, text="Hide", bg='#252824',
                                    fg='white', command=self.fix_action)
        self.fix_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.menu_buttons_frame = tk.Frame(self, bg='#252824')
        self.menu_buttons_visible = False
        self.menu_buttons_height = 20  # Предполагаемая высота кнопок меню

        button = tk.Button(self.menu_buttons_frame, text='Tomorrow', bg='#252824',
                           fg='white',
                           command=self.tomorrow_action)
        button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        button = tk.Button(self.menu_buttons_frame, text='History',
                           bg='#252824',
                           fg='white',
                           command=self.history_action)
        button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        button = tk.Button(self.menu_buttons_frame, text='WB',
                           bg='#252824',
                           fg='white',
                           command=self.wb_action)
        button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        button = tk.Button(self.menu_buttons_frame, text='⚙',
                           bg='#252824',
                           fg='white',
                           command=self.setting_action)
        button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.timer_event = self.after(1000, self.update_timer)
        self.set_window_position()


    def set_window_position(self):
        self.update_idletasks()
        self.set_always_on_top()
        self.is_fixed = True
        self.geometry(f"-2-32")

    def update_timer(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.after_cancel(self.timer_event)
            self.stop()
        else:
            self.label.config(text="     " + self.format_time(self.time_remaining) + "  |  " + self.description)
            self.timer_event = self.after(1000, self.update_timer)


    def today_action(self):
        """
        При нажатии на Today
        1) Если нет файла расписания на сегодня, то он создается с нужным
        именем и помещается в папку now; Открывается excel для составления
        расписания на сегодня
        2) При повторном нажатии на кнопку, если открыт excel, выполняется
        проверка расписания и выводится сообщение о результате проверки.
        Если оно прошло проверку, то парсится в БД и активируется в качестве
        текущего расписания.

        """
        # Получаем нужное имя файла, затем путь к нему
        name_file = get_name_day('today')
        path_d_now: str = path_to_now + '\\' + name_file

        # Проверяем, открыт ли уже файл today
        check_result: list[bool, str] = [False, '']
        if is_excel_file_open(path_d_now):
            # Выполняем базовую проверку новой версии файла
            check_result_one = base_check(template_path=path_day_temp,
                                      day_path=path_d_now,
                                      sheet_name='detailed',
                                      start_orgapp='4:00',
                                      sleep_time='21:30', min_wb=10,
                                      planning_dur='00:10',
                                      path_db=path_to_db, wb_table_name='wb')
            # Получаем текущую дату
            today_date = datetime.now()
            # Форматируем дату в нужный формат 'dd.mm.yy'
            today_date = today_date.strftime('%d.%m.%y')

            get_days_from_db(today_date, 'last')

            # Извлекаем old_shedule, new_shedule, all_wb в виде списков кортежей,
            #   в целях дальнейшей проверки нового расписания
            old_shedule: list[tuple] =
            new_shedule: list[tuple] = parse_table(path_d_now)
            all_wb: list[tuple] = extract_db(select_column='*', path_db=path_to_db, table_name='wb')

            # TODO: Выполняем продвинутую проверку для сегодняшнего расписания
            check_result_two = dur_shift_check(old_shedule=, new_shedule=, all_wb=)

            # Получаем результат с учетом обоих проверок
            check_result[0] = check_result_one[0] and check_result_two[0]
            check_result[1] = check_result_one[1] + '\n' + check_result_two[2]
            # Если все "ок" - сохраняем новую версию файла в БД;
            if check_result[0]:
                # Сначала получаем сегодняшнюю дату
                date_today = datetime.now()
                # Форматируем дату в нужный формат
                # TODO: Может r поставить r'%d.%m.%y'?
                date_today = date_today.strftime('%d.%m.%y')
                # TODO: !!! Учесть first_launch !!!
                # Сохраняем в БД
                add_day_schedule(date=date_today,
                                 path_schedule=path_d_now,
                                 enough_time=True, first_launch=False)

            # Создаем экземпляр класса для показа уведомления
            # TODO: В одном приложении используются разные библиотеки для
            #  показа уведомлений - поправить потом (не критично)
            notif = ToastNotifier()
            # Выводим уведомление о результате проверки
            notif.show_toast(
                title="orgApp",
                msg=check_result[1],
                duration=10,
                threaded=True
            )

            # TODO: !!! Перезагружаем orgApp под новое расписание
            pass

        else:
            # Проверяем, есть ли файл с нужным именем в папке now,
            #   если нет - он создается перед открытием
            if not os.path.exists(path_d_now):
                # Копируем из templates и вставляется с нужным именем
                source_file_path = path_to_clean_templates + '\\' + 'Day.xlsx'
                shutil.copyfile(source_file_path, path_d_now)
            # Открываем файл
            os.startfile(path_d_now)


    def temp_action(self):
        os.startfile(r'C:\Code\orgApp Dev\resources\templates\day_templates')


    def tomorrow_action(self):
        """ При первом нажатии открывает файл excel с расписанием на день
        или если его еще нет - создает на основе пустого шаблона. При
        повторном нажатии, проверяет расписание и если все ок - сохраняет
        его в БД и выводит сообщение, что все ок. Если расписание не прошло
        проверку - выводит сообщение об ошибке и ее причинах.
        """

        # Получаем нужное имя файла, затем путь к нему
        name_file = get_name_day('tomorrow')
        path_d_future: str = path_to_future + '\\' + name_file

        # Проверяем, открыт ли уже файл tomorrow
        # TODO: !!! Функция не сработает, если wps ранее был уже открыт,
        #  чтобы исправить - нужно закрыть сначала wps, затем уже открыть
        check_result: list = []
        if is_excel_file_open(path_d_future):
            # Выполняем проверку новой версии файла
            check_result = base_check(template_path=path_day_temp,
                                      day_path=path_d_future,
                                      sheet_name='detailed', start_orgapp='4:00',
                                      sleep_time='21:30', min_wb=10,
                                      planning_dur='00:10',
                                      path_db=path_to_db, wb_table_name='wb')

            # Если все "ок" - сохраняем новую версию файла в БД;
            if check_result[0]:
                # Сначала получаем завтрашнюю дату
                date_tomorrow = datetime.now() + timedelta(days=1)
                # Форматируем дату в нужный формат
                date_tomorrow = date_tomorrow.strftime('%d.%m.%y')
                # Сохраняем в БД
                add_day_schedule(date=date_tomorrow,
                                 path_schedule=path_d_future,
                                 enough_time=True, first_launch=False)

            # Создаем экземпляр класса для показа уведомления
            # TODO: В одном приложении используются разные библиотеки для
            #  показа уведомлений - поправить потом (не критично)
            notif = ToastNotifier()
            # Выводим уведомление о результате проверки
            notif.show_toast(
                title="orgApp",
                msg=check_result[1],
                duration=10,
                threaded=True
            )

        else:
            # Проверяем, есть ли файл с нужным именем в папке future,
            #   если нет - он создается перед открытием
            if not os.path.exists(path_d_future):
                # Копируем из templates и вставляется с нужным именем
                source_file_path = path_to_clean_templates + '\\' + 'Day.xlsx'
                shutil.copyfile(source_file_path, path_d_future)
            # Открываем файл
            os.startfile(path_d_future)


    def history_action(self):
        os.startfile(r'C:\Code\orgApp Dev\resources\history')


    def wb_action(self):
        # TODO: !!! Похоже он не правильно возвращает вид excel - сдвигая
        #  значения (вроде как уже исправил - проверить)
        db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
        wb_excel = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'
        # Проверяем, что файл открыт
        if is_excel_file_open(
                r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'):
            # Проверяем, что сейчас РБ "development orgApp" или
            #   "setting orgApp"
            if (self.description == 'development orgApp' or self.description ==
                    'setting orgApp'):
                print('Сохранение WB разрешено')
                # Сохранение WB в БД
                # TODO: Протестировать - даст ли он сохранить, если excel
                #  открыт пользователем (вроде должно работать, т.к. по-сути
                #  просто читает excel)
                parse_wb(db, wb_excel)
                notification.notify(
                    title='orgApp',
                    message='Таблица была успешно сохранена в БД'
                )
            else:
                notification.notify(
                    title='Сохранение WB НЕ разрешено',
                    message='Возвращен прежний вид таблицы work_blocks'
                )
                # Вернуть excel в состояние, как в БД
                wb_db_in_excel(db, wb_excel)
        else:
            # Открываем файл
            os.startfile(
                r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx')




    def setting_action(self):

        setting_excel = (r'C:\Code\orgApp Dev\resources\settings\settings.xlsx')

        # TODO: Далее просто копия кнопки WB (поменять!!!) реализовать в
        #  версии v2
        print('Доступ к настройкам будет реализован в версии v2')
        notification.notify(
            message='Доступ к настройкам будет реализован в версии v2'
        )

        # db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
        #
        # # Проверяем, что файл открыт
        # if is_excel_file_open(
        #         r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'):
        #     # Проверяем, что сейчас РБ "development orgApp" или
        #     #   "setting orgApp"
        #     if (self.description == 'development orgApp' or self.description ==
        #             'setting orgApp'):
        #         print('Сохранение WB разрешено')
        #         # Сохранение WB в БД
        #         parse_wb(db, setting_excel)
        #     else:
        #         print('Сохранение WB НЕ разрешено')
        #         notification.notify(
        #             title='Сохранение WB НЕ разрешено',
        #             message='Возвращен прежний вид таблицы work_blocks'
        #         )
        #         # Вернуть excel в состояние, как в БД
        #         wb_db_in_excel(db, setting_excel)
        # else:
        #     # Открываем файл
        #     os.startfile(
        #         r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx')



    def menu_action(self, action=None):
        """
            Обрабатывает нажатие на кнопку "Menu". Если action не None, то была нажата
            одна из дополнительных кнопок меню, и метод просто печатает название этой кнопки.
            В противном случае метод отображает или скрывает дополнительные кнопки меню и
            корректирует положение окна.

            При первом нажатии на "Menu":
            - Отображает кнопки "Tomorrow", "History", "WB", "Settings" внизу окна.
            - Увеличивает высоту окна, чтобы вместить новые кнопки.
            - Поднимает окно вверх на высоту новых кнопок, чтобы окно оставалось на месте.

            При повторном нажатии на "Menu":
            - Скрывает дополнительные кнопки.
            - Восстанавливает исходную высоту окна.
            - Опускает окно на высоту скрытых кнопок, чтобы окно оставалось на месте.

            Параметры:
            - action (str, optional): Название кнопки, если была нажата одна из дополнительных кнопок.
            """
        if action:
            print(f"{action} button pressed")
        else:
            x, y = self.winfo_x(), self.winfo_y()
            if self.menu_buttons_visible:
                # Скрываем кнопки меню и возвращаем окно в исходное положение
                self.menu_buttons_frame.pack_forget()
                self.geometry(f"180x40+{x}+{y + 40}")
            else:
                # Отображаем кнопки меню и поднимаем окно вверх
                self.menu_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)
                self.geometry(f"180x80+{x}+{y - 40}")
            self.menu_buttons_visible = not self.menu_buttons_visible


    def activate_window(self):
        try:
            win32gui.SetForegroundWindow(self.hwnd)
        except Exception as e:
            print(f"Error: {e}")

    def fix_action(self):
        if not self.is_fixed:
            self.fix_button.config(text="Hide")
            self.set_always_on_top()
            self.is_fixed = True
        else:
            self.fix_button.config(text="Fix")
            self.unset_always_on_top()
            self.is_fixed = False

    def set_always_on_top(self):
        windows = get_open_windows_with_processes()
        for hwnd, window_text, process_name, pid in windows:
            if window_text == 'CountdownTimer':
                self.hwnd = hwnd
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def unset_always_on_top(self):
        windows = get_open_windows_with_processes()
        for hwnd, window_text, process_name, pid in windows:
            if window_text == 'CountdownTimer':
                self.hwnd = hwnd
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    @staticmethod
    def parse_time(time_str):
        try:
            minutes, seconds = map(int, time_str.split(":"))
            return minutes * 60 + seconds
        except ValueError:
            raise ValueError("Неверный формат времени. Используйте формат 'мм:сс'.")

    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    @staticmethod
    def trim_description(description):
        if len(description) > 25:
            return description[:25]
        return description

    def stop(self):
        self.destroy()


def run_wb(dur_min_sec, wb_title):
    wb_root = CountdownTimer(dur_min_sec, wb_title)
    wb_root.mainloop()


if __name__ == '__main__':
    app = CountdownTimer('10:00', 'development orgApp')
    app.mainloop()

    # # тестируем сохранение wb в БД
    # db = r'C:\Code\orgApp Dev\resources\db\orgApp.db'
    # wb_excel = r'C:\Code\orgApp Dev\resources\settings\work_blocks.xlsx'
    # parse_wb(db, wb_excel)
    # notification.notify(
    #     title='Сохранение WB разрешено',
    #     message='Таблица была успешно сохранена в БД'
    # )

