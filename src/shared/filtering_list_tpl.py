from typing import Any


def filtering_list_tpl(input_lst_tpl: list[tuple], index_filter: int, value_filter: Any) -> list[tuple]:
    """ 
    Создает копию списка кортежей из другого списка кортежей, оставляя только те кортежи, которые содержат по указанному индексу index_filter значение равное value_filter. 
    
    Порядок кортежей сохраняется, убираются только не подходящие по условию кортежи 
    """

    output_lst_tpl: list[tuple] = []

    for tpl in input_lst_tpl:
        if tpl[index_filter] == value_filter:
            output_lst_tpl.append(tpl)

    return output_lst_tpl
