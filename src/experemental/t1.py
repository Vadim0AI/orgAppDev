import multiprocessing
from src.organizer.interface.wb_timer import CountdownTimer
import time

def my_function(duration, wb_title):
    wb_root = CountdownTimer(duration, wb_title)
    wb_root.mainloop()


if __name__ == '__main__':
    # Создаем процесс и передаем ему функцию и аргументы
    process = multiprocessing.Process(target=my_function, args=(10, 20))

    # Запускаем процесс
    process.start()

    for i in range(10):
        print(i)
        time.sleep(1)

    process.terminate()