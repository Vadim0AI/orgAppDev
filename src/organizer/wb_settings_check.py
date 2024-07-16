

def wb_settings_check(template_settings: dict[tuple], wb_setting: dict[tuple]) -> bool:
    """ 
    Проверяет, соответсвет ли полученная настройка Рабочего Блока wb_setting шаблону настроек template_settings.

    # TODO: Пока функция просто сравнивает словари - сложные комбинации и пересечения внутри значений настроек не учитываются. Порядок значений настроек также должен строго соответствовать друг другу.
    """
    # Перебираем настройки шаблона
    for setting_name, setting_val in template_settings.items():
        # Если есть несоответсвие настройки шаблона - возвращаем False
        if wb_setting[setting_name] != setting_val:
            return False
        
    return True
