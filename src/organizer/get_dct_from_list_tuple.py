

def get_dct_from_list_tuple(lst_tpl: list[tuple], key_index: int) -> dict[tuple]:
    """
    Превращает список кортежей в словарь, в параметре указываем индекс кортежей, по которому соответствующие кортежи будут превращены в ключи словаря.
    При этом значения в словарь переносятся полностью, в том числе с ключом словаря.
    """
    result_dct = {}
    for tpl in lst_tpl:
        if key_index >= len(tpl):
            raise IndexError(f"Индекс {key_index} превышает длину кортежа {tpl}")
        key = tpl[key_index]
        result_dct[key] = tpl
    return result_dct


if __name__ == '__main__':
    lst_tpl = [
    (1, 'a', 'b'),
    (2, 'c', 'd'),
    (3, 'e', 'f')
]

key_index = 0
result_dct = get_dct_from_list_tuple(lst_tpl, key_index)
print(result_dct)
key_index = 2
result_dct = get_dct_from_list_tuple(lst_tpl, key_index)
print(result_dct)
key_index = 3
result_dct = get_dct_from_list_tuple(lst_tpl, key_index)
print(result_dct)
