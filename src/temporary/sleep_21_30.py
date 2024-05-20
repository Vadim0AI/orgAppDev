import pytz
from datetime import datetime

# Указываем часовой пояс Екатеринбурга
ekaterinburg_timezone = pytz.timezone('Asia/Yekaterinburg')

# Получаем текущее время в часовом поясе Екатеринбурга
current_time = datetime.now(ekaterinburg_timezone)

# Получаем часы и минуты из текущего времени
current_hour = current_time.hour
current_minute = current_time.minute

print("Текущее время в Екатеринбурге:", current_hour, "часов", current_minute, "минут")
