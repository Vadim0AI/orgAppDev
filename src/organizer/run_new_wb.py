import multiprocessing
from src.organizer.interface.new_wb import app_new_wb



def run_new_wb(dur_min_sec, wb_title):
    # Запускаем таймер newWB в новом процессе
    process_new_wb = multiprocessing.Process(target=app_new_wb,
                                               args=(dur_min_sec, wb_title))
    process_new_wb.start()

    return process_new_wb


if __name__ == '__main__':
    p = run_new_wb('00:10', 'test')
    print(p)