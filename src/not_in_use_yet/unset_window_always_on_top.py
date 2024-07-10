import win32gui
import win32con



def unset_window_always_on_top(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_NOTOPMOST,  # Убираем окно с позиции поверх всех
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE  # Не меняем размер и положение
    )