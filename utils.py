def get_int_val(text: str, size: int) -> int:
    """
    Проверяет и возвращает число (это может быть необходимо когда вы хотите проверить,
        что пользователь ввел именно число и это число лежит в диапазоне border[0] и border[1]).
        Спрашиваем у пользователя ввод числа с текстом text и проверяем что оно соответствует требованиям, если не
        соответствует хотя бы одному требованию, то заново просим ввести число.

    :param text: Текст перед получением числа
    :param border: Ограничение на число (минимум, максимум)
    :return: Возвращает число, которое ввёл пользователь и прошедшее все проверки
    """

    border = [1, size ** 2]
    while True:

        if text.isdigit() and min(border) <= int(text) <= max(border):
            return text

        text = input("Вы ввели недопустимый символ или число. Введите допуcтимое число: ")


def is_win(size: int) -> tuple:
    """
    Функция передает выигрышные комбинации в зависимости от размера игрового поля
    :param size: размер стороны игрового поля
    :return: кортеж кортежей выигрышных комбинаций
    """

    win_comb = []

    # Перебор выигрышных комбинации
    for i in range(size):
        win_comb.append(tuple(range((i) * size, size * (i + 1))))  # горизонтальные комбинации
    for i in range(size):
        win_comb.append(tuple(range(i, size ** 2 + i, size)))  # вертикальные комбинации

    win_comb.append(tuple(range(0, size ** 2, size + 1)))  # левая диагональ
    win_comb.append(tuple(range(size - 1, size ** 2 - 1, size - 1)))  # правая диагональ

    return tuple(win_comb)

game_types = {
    "1": {"type": "friend", "description": "Игра с другом", "player_count": 2},
    "2": {"type": "computer", "description": "Игра с компьютером", "player_count": 1},
}

if __name__ == "__main__":
    print(get_int_val("10", 4))
    # print(is_win(5))