from time import struct_time


def ch_t_interval(now: struct_time, beginning: struct_time,
                  end: struct_time) -> bool:
    """
    Сокр. от Check time interval.
    Проверяет, принадлежит ли указанное время интервалу.

    Args:
    now (obj struct_time): Время, которое нужно проверить на принадлежность
    интервалу.
    beginning (struct_time): Время начала интервала.
    end (struct_time): Время окончания интервала.

    Returns:
    bool: True, если полученное время соответствует полученному интервалу
    времени, иначе False.
    """
    return beginning <= now <= end