import win32gui
import psutil


def list_windows():
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            results.append((hwnd, win32gui.GetWindowText(hwnd)))

    results = []
    win32gui.EnumWindows(enum_callback, results)
    return results

if __name__ == "__main__":
    windows = list_windows()
    for hwnd, title in windows:
        print(f"Window handle: {hwnd}, Title: {title}")

    for proc in psutil.process_iter():
        print(proc.name())