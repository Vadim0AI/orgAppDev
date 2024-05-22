def hex_to_rgba(hex_color, alpha=1):
    """Преобразует цвет из формата hex в формат RGBA."""
    # Удаляем символ # и разбиваем на каналы
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    # Преобразуем значения каналов в диапазон от 0 до 1
    rgba_color = (r / 255.0, g / 255.0, b / 255.0, alpha)
    return rgba_color

# # Пример использования
# hex_color = '#bc82f9'
# rgba_color = hex_to_rgba(hex_color)
# print("Цвет в формате RGBA:", rgba_color)
