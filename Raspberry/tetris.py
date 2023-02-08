import os
from typing import List, Tuple

from random import randint, choice

from pynput import keyboard
from time import sleep

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
random_piece = lambda: choice([I, O, T, L, J, S, Z])
is_line_full = lambda matrix, y: all(matrix[y])
is_first_line_empty = lambda matrix: all([x == 0 for x in matrix[0]])

# give a size to the matrix who represent the game
n = 20  # number of lines # * le vrai tableau fait 40 lignes
p = 10  # number of columns# * le vrai tableau fait 30 colonnes

# give a time between each turn
frame_per_seconds = 10

# list of matrix who represent tetris pieces who can use in game (T, L, J, S, Z, I, O)
I = [[1, 1, 1, 1]]
O = [[2, 2], [2, 2]]
T = [[3, 3, 3], [0, 3, 0]]
L = [[4, 4, 4], [4, 0, 0]]
J = [[5, 5, 5], [0, 0, 5]]
Z = [[6, 6, 0], [0, 6, 6]]
S = [[0, 7, 7], [7, 7, 0]]

# black - cyan - yellow - purple - grey - blue - red - green - white
colors = [(0, 0, 0), (0, 255, 255), (255, 255, 0), (128, 0, 128), (128, 128, 128), (0, 0, 255), (255, 0, 0),
          (0, 255, 0), (255, 255, 255)]


# give the touch who can use in game
left = 'KEY_LEFT'
right = 'KEY_RIGHT'
down = 'KEY_DOWN'
rotate = 'KEY_UP'
arrow_keys = {
    "KEY_UP": {
        "code": 126,
        "state": False
    },
    "KEY_DOWN": {
        "code": 125,
        "state": False
    },
    "KEY_LEFT": {
        "code": 123,
        "state": False
    },
    "KEY_RIGHT": {
        "code": 124,
        "state": False
    }
}


def on_press(key):
    if key == keyboard.Key.up:
        arrow_keys["KEY_UP"]["state"] = True
    elif key == keyboard.Key.down:
        arrow_keys["KEY_DOWN"]["state"] = True
    elif key == keyboard.Key.left:
        arrow_keys["KEY_LEFT"]["state"] = True
    elif key == keyboard.Key.right:
        arrow_keys["KEY_RIGHT"]["state"] = True
    else:
        pass


def on_release(key):
    if key == keyboard.Key.up:
        arrow_keys["KEY_UP"]["state"] = False
    elif key == keyboard.Key.down:
        arrow_keys["KEY_DOWN"]["state"] = False
    elif key == keyboard.Key.left:
        arrow_keys["KEY_LEFT"]["state"] = False
    elif key == keyboard.Key.right:
        arrow_keys["KEY_RIGHT"]["state"] = False
    else:
        pass


# Collect events until released
listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
listener.start()


def display_on_console(array: List[List[int]]) -> None:
    """
    Display the array on the bash terminal with colors and █ characters
    :param array: array to display
    :return: None
    """
    for y in range(len(array)):
        for x in range(len(array[y])):
            color = colors[array[y][x]]
            print(f"\033[48;2;{color[0]};{color[1]};{color[2]}m  ", end="")
        print("\033[0m")


def place_piece(matrix, piece, x, y):
    """
    Place a piece in the matrix at the coordinates (x, y)
    :param matrix: matrix to place the piece
    :param piece: piece to place
    :param x: x coordinate
    :param y: y coordinate
    :return: matrix with the piece placed
    """
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                matrix[y + i][x + j] = piece[i][j]
    return matrix


def delete_piece(matrix, piece, x, y):
    """
    Delete a piece in the matrix at the coordinates (x, y)
    :param matrix: matrix to delete the piece
    :param piece: piece to delete
    :param x: x coordinate
    :param y: y coordinate
    :return: matrix with the piece deleted
    """
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                matrix[y + i][x + j] = 0
    return matrix


def can_move_left(matrix, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                if x + j - 1 < 0 or matrix[y + i][x + j - 1] != 0:
                    return False
    return True


def can_move_right(matrix, piece, x, y):
    """
    Check if the piece can move to the right
    :param matrix: matrix to check
    :param piece: piece to check
    :param x: x coordinate of the piece
    :param y: y coordinate of the piece
    :return: True if the piece can move to the right, False otherwise
    """

    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                if x + j + 1 >= len(matrix[y]) or matrix[y + i][x + j + 1] != 0:
                    return False
    return True


def delete_full_lines(matrix):
    """
    Delete all full lines in the matrix
    :param matrix: matrix to delete the lines
    :return: matrix with the lines deleted
    """
    y = 0

    def delete_line(matrix, y):
        """
        Delete a line in the matrix
        :param matrix: matrix to delete the line
        :param y: y coordinate of the line to delete
        :return: matrix with the line deleted
        """
        for i in range(y, 0, -1):
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i - 1][j]
        return matrix

    def descend_pieces(matrix):
        """
        Descend all pieces in the matrix while it is possible
        :param matrix: matrix to descend the pieces
        :return: matrix with the pieces descended
        """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    while i < len(matrix) - 1 and matrix[i + 1][j] == 0:
                        matrix[i + 1][j] = matrix[i][j]
                        matrix[i][j] = 0
                        i += 1
        return matrix

    while y < len(matrix):
        if is_line_full(matrix, y):
            matrix = delete_line(matrix, y)
            matrix = descend_pieces(matrix)
        else:
            y += 1

    return matrix


def can_descend(matrix, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0 and not (i + 1 < len(piece) and piece[i + 1][j] != 0):
                if y + i + 1 == len(matrix) or matrix[y + i + 1][x + j] != 0:
                    return False
    return True


def turn_piece(piece):
    """
    Turn a piece
    :param piece: piece to turn
    :return: turned piece
    """
    new_piece = []
    for i in range(len(piece[0])):
        new_piece.append([])
        for j in range(len(piece)):
            new_piece[i].append(piece[j][i])
    new_piece.reverse()
    return new_piece


def main():
    matrix = [[0 for _ in range(p)] for _ in range(n)]

    current_tetrominos = random_piece()
    x = randint(0, p - 4)
    y = 0

    continued = False

    print("*--------------*")
    print("| Tretris Game |")
    print("*--------------*")

    while is_first_line_empty(matrix):
        if not can_descend(matrix, current_tetrominos, x, y):
            # if the tetrominos cannot go down then we check for any full line to score then we create a new tetrominos
            matrix = delete_full_lines(matrix)
            current_tetrominos = random_piece()
            x = randint(0, p - 4)
            y = 0
            if continued:
                break
            continued = True
            continue

        continued = False
        matrix = delete_piece(matrix, current_tetrominos, x, y)
        if arrow_keys["KEY_LEFT"]["state"] and can_move_left(matrix, current_tetrominos, x, y):
            x -= 1
        elif arrow_keys["KEY_RIGHT"]["state"] and can_move_right(matrix, current_tetrominos, x, y):
            x += 1
        elif arrow_keys["KEY_DOWN"]["state"]:
            y -= 1
        elif arrow_keys["KEY_UP"]["state"]:
            current_tetrominos = turn_piece(current_tetrominos)

        y += 1
        matrix = place_piece(matrix, current_tetrominos, x, y)
        display_on_console(matrix)
        sleep(1 / frame_per_seconds)
        clear()
    display_on_console(matrix)
    listener.stop()
    print("Game Over")


if __name__ == '__main__':
    main()
