import tkinter as tk
from tkinter import messagebox
import win32gui
import win32con
from src.organizer.get_open_windows_with_processes import get_open_windows_with_processes



class CountdownTimer:
    def __init__(self, time_remaining, description):
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        self.time_remaining = self.parse_time(time_remaining)
        self.description = self.trim_description(description)
        self.is_fixed = False  # Добавляем переменную состояния
        self.menu_visible = False  # Добавляем переменную для видимости меню
        self.hwnd = None  # Хранит уникальный дескриптор окна
        self.create_widgets()
        self.set_window_position()
        self.update_timer()

    def create_widgets(self):
        self.root.configure(bg='#252824')
        self.root.geometry('280x60')
        self.root.overrideredirect(True)

        self.label = tk.Label(self.root, text="     " + self.format_time(self.time_remaining) + "  |  " + self.description,
                              bg='#252824', fg='white', font=('Arial', 12), anchor='w')
        self.label.pack(fill='both', expand=True)

        buttons_frame = tk.Frame(self.root, bg='#252824')
        buttons_frame.pack(fill='x')

        self.menu_button = tk.Button(buttons_frame, text='Menu', bg='#4f4f4f', fg='white', bd=0, command=self.menu_action)
        self.menu_button.pack(side='left', padx=5)

        self.update_button = tk.Button(buttons_frame, text='Tomorrow', bg='#4f4f4f', fg='white', bd=0, command=self.update_action)
        self.update_button.pack(side='left', padx=5)

        self.fix_button = tk.Button(buttons_frame, text='Hide', bg='#4f4f4f', fg='white', bd=0, command=self.fix_action)
        self.fix_button.pack(side='right', padx=5)

    def set_window_position(self):
        self.root.update_idletasks()
        x = 618
        y =
        self.root.geometry(f"+{x}+{y}")
        self.root.lift()

    def activate_window(self):
        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

    def update_timer(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            messagebox.showinfo("Countdown Timer", "Time's up!")
            self.root.destroy()
        else:
            self.label.config(text="     " + self.format_time(self.time_remaining) + "  |  " + self.description)
            self.root.after(1000, self.update_timer)

    def menu_action(self):
        if self.menu_visible:
            self.root.geometry('280x60')
            self.menu_visible = False
        else:
            self.root.geometry('280x90')
            self.menu_visible = True
        self.set_window_position()

    def update_action(self):
        print("Update button pressed")

    def fix_action(self):
        if not self.is_fixed:
            self.fix_button.config(text='Fix')
            self.is_fixed = True
        else:
            self.fix_button.config(text='Hide')
            self.is_fixed = False

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

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    CountdownTimer('10:00', 'Countdown').run()
