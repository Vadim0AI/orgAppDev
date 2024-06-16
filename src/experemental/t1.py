import win32gui
import win32con

hwnd = 0  # Замените на обработчик окна, который вы хотите отображать сообщение
win32gui.MessageBox(hwnd, "Title", "Message", win32con.MB_OK)