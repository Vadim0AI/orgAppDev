from src.organizer.permissions.orgApp_close import kill_process_by_name
from time import sleep
import threading

# TODO: Модуль не доделан

def blocked_process_by_name(process_name):
    while True:
        for process in process_name:
            kill_process_by_name(process)
        sleep(3)


def orgApp_blocked(process_name):
    # Создание потока
    thread = threading.Thread(target=blocked_process_by_name, args=(process_name,))
    # Запуск потока
    thread.start()


processes = ["Taskmgr.exe", "mmc.exe", "SystemSettings.exe", "vadiktxt.exe"]
orgApp_blocked(processes)

print(3)
a = 84
b = 32
c = a**b
print(c)

while True:
    print(b**a, '\n')
    sleep(2)
