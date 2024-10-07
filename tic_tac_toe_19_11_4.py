"""
Задание на проект крестики-нолики.

Создать консольное приложение крестики-нолики.

Необходимо реализовать функциональность игры двух людей, сначала играет первый человек, потом второй.
Реализация игры с компьютером по желанию и не является обязательным требованием.

Желательно если ваша реализация не будет привязана к полю 3x3, т.е. если я захочу сыграть на поле размером 4x4,
то мне максимум нужно будет только изменить размер поля, а код менять не нужно. Однако, если данная задача является
сложной на данном этапе, то можно зафиксировать размер поля.

Приложение должно быть разбито на функции, отвечающие за свою функциональность.

Необходимо провести описание функции, её входных переменных и провести аннотацию входных и выходных переменных.

Ниже приведен прототип приложения можно его использовать для заполнения или можно сделать свою структуру.

"""
import random
from typing import Union, Optional
import utils

print("Добро пожаловать в игру КРЕСТИКИ_НОЛИКИ")

EMPTY_CELL = " "
while True:
    SIZE_FIELD = input("Введите размер игрового поля: ")
    if not SIZE_FIELD.isdigit():
        SIZE_FIELD = utils.get_int_val(SIZE_FIELD, 10)
    if SIZE_FIELD != "0" and SIZE_FIELD != "1" or int(SIZE_FIELD) < 0:
        break
    else:
        print("Недопустимый размер игрового поля!")
        continue

size = int(SIZE_FIELD)
field = list(range(1, size ** 2 + 1))


def draw_field(field: list[int]) -> None:
    """
    Функция рисует поле
    :param field: список с ячейками поля
    :return: None. Выводит визуальное представление игрового поля
    """
    count = 0
    for i in range(size):
        print("_______" * size + "_")
        print("| ", end="")
        for j in range(size):
            print(f"{field[count] :^4}", end=" | ")
            count += 1
        print()
    print("_______" * size + "_")
    print("нумерация ячеек для ходов")


def get_index_from_table(field: list[int], size: int) -> int:
    """
    Проверка ячейки на занятость.
    Спрашиваем у пользователя куда он хочет поставить, проверяем свободна ли ячейка, если занята,
        то просим заново выбрать куда поставить
    :param field: игровое поле в виде списка
    :param size: размер стороны игрового поля
    :return: Возвращаем номер свободной ячейки
    """

    # разбиваем список на строки и выводим в консоль
    count = 0
    for i in range(size):
        print("|", end="")
        for j in range(size):
            print(f"{field[count] : 4}", end=" | ")
            count += 1
        print()
    #  Спрашиваем у пользователя куда он хочет поставить,
    #  проверяем свободна ли ячейка, если занята,то просим заново выбрать куда поставить
    index_step = int(input("Введите номер ячейки, куда Вы хотите сходить: ")) - 1
    while field[index_step] == "X" or field[index_step] == "O":
        index_step = int(input(f"Ячейка {index_step} занята, укажите другую ячейку")) - 1

    return index_step


def set_player_in_field(field: list[int], current_player: str, index_step=None) -> list[str]:
    """
    Реализация игрового процесса
    Ставим игрока на поле. По переданным координатам index_step ставим игрока current_player на поле field
    :param field:
    :param current_player:

    :return: Возвращаем поле с текущим ходом игрока
    """

    players = ("X", "O")
    step = 0
    while step < size ** 2:
        index_step_str = input(f'Игрок "{current_player}" ведите номер ячейки для ввода: ')
        # обращаемся к функции get_int_val() для проверки корректности введенного числа
        index_step = int(utils.get_int_val(index_step_str, size)) - 1
        while field[index_step] == "X" or field[index_step] == "O":
            index_step_str = input(f'Ячейка "{index_step + 1}" занята, укажите другую ячейку: ')
            # обращаемся к функции utils.get_int_val() для проверки корректности введенного числа
            index_step = int(utils.get_int_val(index_step_str, size)) - 1

        field[index_step] = current_player
        current_player = players[players.index(current_player) - 1]

        # разбиваем список на строки и выводим в консоль
        count = 0
        for i in range(size):
            print("_______" * size + "_")
            print("| ", end="")
            for j in range(size):
                print(f"{field[count] :^4}", end=" | ")
                count += 1
            print()
        print("_______" * size + "_")
        step += 1
        print("шаг игры - ", step)
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей

        # Определяем выигрышная ли комбинация, вводим переменную и подключаем функцию iswin()
        win = is_win(field)
        if win:
            print(f'Игра окончена, ходов больше нет, победил игрок "{players[players.index(current_player) - 1]}"')
            break
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей
        elif step == size ** 2:
            print("Игра окончена, ходов больше нет. Ничья")
            break

    return field


def playing_with_computer(field: list[int], current_player: str, index_step=None) -> list[str]:
    """
    Реализация игрового процесса c с ходом компьютера
    Ставим игрока на поле. По переданным координатам index_step ставим игрока current_player на поле field
    :param field:
    :param current_player:

    :return: Возвращаем поле с текущим ходом игрока
    """

    players = ("X", "O")
    step = 0
    while step < size ** 2:
        # ХОД ЧЕЛОВЕКА
        index_step_str = input(f'Игрок "{current_player}" ведите номер ячейки для ввода: ')
        # обращаемся к функции get_int_val() для проверки корректности введенного числа
        index_step = int(utils.get_int_val(index_step_str, size)) - 1
        while field[index_step] == "X" or field[index_step] == "O":
            index_step_str = input(f'Ячейка "{index_step + 1}" занята, укажите другую ячейку: ')
            # обращаемся к функции utils.get_int_val() для проверки корректности введенного числа
            index_step = int(utils.get_int_val(index_step_str, size)) - 1

        field[index_step] = current_player
        current_player = players[players.index(current_player) - 1]

        # разбиваем список на строки и выводим в консоль
        count = 0
        for i in range(size):
            print("_______" * size + "_")
            print("| ", end="")
            for j in range(size):
                print(f"{field[count] :^4}", end=" | ")
                count += 1
            print()
        print("_______" * size + "_")
        step += 1
        print("шаг игры - ", step)
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей

        # Определяем выигрышная ли комбинация, вводим переменную и подключаем функцию iswin()
        win = is_win(field)
        if win:
            print(f'Игра окончена, ходов больше нет, победил игрок "{players[players.index(current_player) - 1]}"')
            break
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей
        elif step == size ** 2:
            print("Игра окончена, ходов больше нет. Ничья")
            break

        # ХОД КОМПЬЮТЕРА
        print(f'Игрок "{current_player}" - компьютер" введите номер ячейки для ввода: ')
        index_step = random.choice(field)
        print(field.index(index_step) + 1)
        while index_step == "X" or index_step == "O":
            print(f'Ячейка "{field.index(index_step) + 1}" занята, укажите другую ячейку: ')
            index_step = random.choice(field)
            print(field.index(index_step) + 1)
            continue

        field[index_step-1] = current_player
        current_player = players[players.index(current_player) - 1]

        # разбиваем список на строки и выводим в консоль
        count = 0
        for i in range(size):
            print("_______" * size + "_")
            print("| ", end="")
            for j in range(size):
                print(f"{field[count] :^4}", end=" | ")
                count += 1
            print()
        print("_______" * size + "_")
        step += 1
        print("шаг игры - ", step)
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей

        # Определяем выигрышная ли комбинация, вводим переменную и подключаем функцию iswin()
        win = is_win(field)
        if win:
            print(f'Игра окончена, ходов больше нет, победил игрок "{players[players.index(current_player) - 1]}"')
            break
        # при наборе максимально допустимого количества ходов закрываем цикл While, заканяиваем игру и выодим сообщение о ничьей
        elif step == size ** 2:
            print("Игра окончена, ходов больше нет. Ничья")
            break

    return field


def is_win(field) -> bool:
    """
    Определяем произошла ли победа. Если на текущем поле выигрышная комбинация, то возвращает True. Если никто не выиграл,
        то возвращаем False
    :param field: текущий список с ходами
    :return: False - комбинация не выигрышная, True - комбинация выигрышная
    """

    win = False
    win_comb = utils.is_win(size)

    count_X, count_O = 0, 0
    for win_typ in win_comb:
        for j in win_typ:
            if field[j] == "X":
                count_X += 1

                if count_X == size:
                    win = True
                    break
        count_X = 0
    for win_typ in win_comb:
        for j in win_typ:
            if field[j] == "O":
                count_O += 1
                if count_O == size:
                    win = True
                    break
        count_O = 0
    return win


def change_player() -> str:
    """
    Определяет кто ходит следующий

    :param current_player: случайным выбором определяем очередность
    :return: текцщий игрок, начинающий ход первым
    """

    players = ("X", "O")
    current_player = random.choice(players)
    print(f'Первый ход делает игрок "{current_player}"')

    return current_player


def get_game_type() -> str:
    """
    Получение от пользователя типа игры
    :return: тип игры
    """
    print("Выберете тип игры")
    while True:
        for k, v in utils.game_types.items():
            print(f"{k}. {v['description']}")

        game_type = input("Введите номер типа игры: ")
        if game_type == "1":
            draw_field(field)
            set_player_in_field(field, change_player())
            break
        elif game_type == "2":
            draw_field(field)
            playing_with_computer(field, change_player())
            break
        elif game_type not in utils.game_types.keys():
            print("Выбран неправильный тип игры, повторите ввод ещё раз")
            continue


def app():
    """
    Запуск приложения игры крестики-нолики
    :return: None
    """

    get_game_type()
    # draw_field(field)
    # set_player_in_field(field, change_player())


if __name__ == "__main__":
    app()
