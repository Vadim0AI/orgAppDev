import signal
import sys
from write_log import write_log


def signal_handler(sig, frame):
    print("Хотите ли вы сохранить изменения перед выходом?")
    write_log("Вот здесь система должна быть выключена")
    # Здесь можно добавить код для сохранения данных или выполнения других действий
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while True:
    pass


