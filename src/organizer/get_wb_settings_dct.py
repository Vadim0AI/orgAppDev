from typing import Dict, Tuple


def get_wb_settings_dct(setting: str) -> Dict[str, Tuple[str, ...]]:
    """ Принимает строку из БД wb, поле settings, парсит ее и превращает в словарь.

    Parameters:
    setting_str (str): Пример строки: 'shift : right | duraton : fix'. 
    Одна строка - один РБ (настройки для него). Вертикальная черта с пробелами по бокам - это разделитель различных настроек для РБ ' | '. Разделитель между типом настройки и значением настройки - двоеточие с пробелами по бокам ' : '. Разделитель между разными значениями одной настройки - это запятая с пробелом ', '.
    
    Returns:
    setting_dict (dict): Словарь, где ключ - это настройка РБ, а значения - это кортеж значений настройки.
    """
    setting_dict = {}
    settings = setting.split(' | ')
    for s in settings:
        key, values = s.split(' : ')
        values_list = values.split(', ')
        setting_dict[key.strip()] = tuple(values_list)
    
    return setting_dict


if __name__ == '__main__':
    # Пример 1: Простая строка с одной настройкой
    setting_str1 = 'shift : right'
    result1 = get_wb_settings_dct(setting_str1)
    print(result1)  # {'shift': ('right',)}

    # Пример 2: Строка с несколькими настройками
    setting_str2 = 'shift : right | duration : fix'
    result2 = get_wb_settings_dct(setting_str2)
    print(result2)  # {'shift': ('right',), 'duration': ('fix',)}

    # Пример 3: Строка с несколькими значениями для одной настройки
    setting_str3 = 'shift : right, left | duration : fix, adjust'
    result3 = get_wb_settings_dct(setting_str3)
    print(result3)  # {'shift': ('right', 'left'), 'duration': ('fix', 'adjust')}

    # Пример 4: Строка с пробелами вокруг разделителей
    setting_str4 = ' shift : right | duration : fix '
    result4 = get_wb_settings_dct(setting_str4)
    print(result4)  # {'shift': ('right',), 'duration': ('fix',)}

    # Пример 5: Строка с пустыми значениями
    setting_str5 = 'shift : right, | duration : fix, '
    result5 = get_wb_settings_dct(setting_str5)
    print(result5)  # {'shift': ('right', ''), 'duration': ('fix', '')}
