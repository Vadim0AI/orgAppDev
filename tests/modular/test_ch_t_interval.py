from time import struct_time
from src.experemental.others.shedule.ch_t_interval import ch_t_interval

def test_ch_t_interval_inside():
    now = struct_time((2024, 4, 22, 12, 0, 0, 0, 112, -1))
    beginning = struct_time((2024, 4, 22, 10, 0, 0, 0, 112, -1))
    end = struct_time((2024, 4, 22, 14, 0, 0, 0, 112, -1))
    assert ch_t_interval(now, beginning, end) == True

def test_ch_t_interval_outside():
    now = struct_time((2024, 4, 22, 16, 0, 0, 0, 112, -1))
    beginning = struct_time((2024, 4, 22, 10, 0, 0, 0, 112, -1))
    end = struct_time((2024, 4, 22, 14, 0, 0, 0, 112, -1))
    assert ch_t_interval(now, beginning, end) == False

def test_ch_t_interval_boundary():
    now = struct_time((2024, 4, 22, 14, 0, 0, 0, 112, -1))
    beginning = struct_time((2024, 4, 22, 10, 0, 0, 0, 112, -1))
    end = struct_time((2024, 4, 22, 14, 0, 0, 0, 112, -1))
    assert ch_t_interval(now, beginning, end) == True
