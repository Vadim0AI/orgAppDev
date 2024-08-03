import tkinter as tk
import win32gui
import win32con
from src.organizer.get_open_windows_with_processes import get_open_windows_with_processes



class NewWB(tk.Tk):
    """
        Таймер для переключения на новый РБ.

        Класс NewWB представляет собой окно таймера обратного отсчета, созданное с использованием Tkinter.
        Окно отображает оставшееся время и описание задачи. Оно также может быть зафиксировано поверх других окон
        и включает несколько кнопок для управления.

        Атрибуты:
        - time_remaining (int): Время до завершения таймера в секундах.
        - description (str): Описание задачи, обрезанное до 25 символов.
        - is_fixed (bool): Флаг, указывающий, зафиксировано ли окно поверх других окон.
        - hwnd (int or None): Дескриптор окна для взаимодействия с Win32 API.

        Методы:
        - __init__(self, time_remaining, description, *args, **kwargs): Инициализирует окно с таймером, создаёт виджеты и запускает таймер.
        - set_window_position(self): Устанавливает начальное положение окна и фиксирует его поверх других окон.
        - update_timer(self): Обновляет таймер каждую секунду, завершает его при достижении нуля.
        - update_action(self): Обрабатывает нажатие кнопки "Next" (в данный момент просто печатает сообщение).
        - activate_window(self): Активирует окно, переводя его на передний план.
        - fix_action(self): Переключает состояние фиксации окна поверх других окон.
        - set_always_on_top(self): Устанавливает окно поверх всех других окон.
        - unset_always_on_top(self): Снимает окно с фиксированного верхнего положения.
        - parse_time(time_str): Преобразует строку времени в формат "мм:сс" в секунды.
        - format_time(seconds): Форматирует время в секундах в строку формата "мм:сс".
        - trim_description(description): Обрезает описание задачи до 25 символов.
        - play_sound(self): Воспроизводит звуковое уведомление (в данный момент метод не используется).
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
        self.geometry("180x40")
        self.configure(bg='#252824')
        self.overrideredirect(True)

        self.label = tk.Label(self, text="     " + self.format_time(self.time_remaining) + "  |  " + self.description,
                              bg='#252824', fg='white', anchor='w')
        self.label.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self, bg='#252824')
        button_frame.pack(fill=tk.X)

        self.update_button = tk.Button(button_frame, text="Next", bg='#252824',
                                       fg='white', command=self.next_action)
        self.update_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.fix_button = tk.Button(button_frame, text="Hide", bg='#252824',
                                    fg='white', command=self.fix_action)
        self.fix_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.timer_event = self.after(1000, self.update_timer)
        self.set_window_position()


    def set_window_position(self):
        self.update_idletasks()
        self.set_always_on_top()
        self.is_fixed = True
        # Получаем ширину и высоту экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Вычисляем координаты для центрирования окна
        x = (screen_width - 180) // 2
        y = (screen_height - 40) // 2
        # Устанавливаем размер и положение окна по центру экрана
        self.geometry(f"180x40+{x}+{y}")


    def update_timer(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.after_cancel(self.timer_event)
            self.stop()
        else:
            self.label.config(text="     " + self.format_time(self.time_remaining) + "  |  " + self.description)
            self.timer_event = self.after(1000, self.update_timer)


    def next_action(self):
        self.stop()


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

    def play_sound(self):
        playsound(r'C:\Code\orgApp Dev\resources\sound\notification_new_wb.mp3')

    def stop(self):
        self.destroy()


def app_new_wb(dur_min_sec, wb_title):
    wb_root = NewWB(dur_min_sec, wb_title)
    wb_root.mainloop()


if __name__ == '__main__':
    app = NewWB('1:10', '12345678901234567')
    app.mainloop()
