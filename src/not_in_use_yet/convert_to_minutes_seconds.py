def convert_to_minutes_seconds(time_hh_mm: str):
    t = time_hh_mm.split(':')
    hours = int(t[0])
    minutes = int(t[1])
    new_minutes = hours * 60 + minutes
    return f'{new_minutes}:00'