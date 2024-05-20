import tkinter as tk
import win32gui
import win32con
from src.organizer.get_open_windows_with_processes import get_open_windows_with_processes

class NewWB(tk.Tk):
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
                                      bg='#252824', fg='white', command=self.update_action)
        self.today_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.fix_button = tk.Button(button_frame_1, text="Hide", bg='#252824',
                                    fg='white', command=self.fix_action)
        self.fix_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.menu_buttons_frame = tk.Frame(self, bg='#252824')
        self.menu_buttons_visible = False
        self.menu_buttons_height = 20  # Предполагаемая высота кнопок меню

        for text in ["Tomorrow", "History", "WB", "⚙"]:
            button = tk.Button(self.menu_buttons_frame, text=text, bg='#252824',
                               fg='white', command=lambda t=text: self.menu_action(t))
            button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.timer_event = self.after(1000, self.update_timer)
        self.set_window_position()

    def set_window_position(self):
        self.update_idletasks()
        self.set_always_on_top()
        self.is_fixed = True
        self.geometry(f"+1354+792")

    def update_timer(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.after_cancel(self.timer_event)
            self.stop()
        else:
            self.label.config(text="     " + self.format_time(self.time_remaining) + "  |  " + self.description)
            self.timer_event = self.after(1000, self.update_timer)

    def update_action(self):
        print("Update button pressed")


    def menu_action(self, action=None):
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

    def play_sound(self):
        playsound(r'C:\Code\orgApp Dev\resources\sound\notification_new_wb.mp3')

    def stop(self):
        self.destroy()

if __name__ == '__main__':
    app = NewWB('01:10', 'orgApp')
    # app.attributes('-alpha', 0.75)
    app.mainloop()
