import random
import time
import os
import keyboard

# ?_______________________________________________________________
from colorama import init, Fore, Back, Style

init()
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
BRIGHTNESS = [Style.DIM, Style.NORMAL, Style.BRIGHT]


def print_with_white(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_red(s, color=Fore.RED, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_green(s, color=Fore.GREEN, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_yellow(s, color=Fore.YELLOW, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_blue(s, color=Fore.BLUE, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_magenta(s, color=Fore.MAGENTA, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_cyan(s, color=Fore.CYAN, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def print_with_grey(s, color=Fore.WHITE, brightness=Style.DIM, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


# create a function who print the matrix in the console
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                print('□', end=' ')
            elif matrix[i][j] == 1:
                print_with_cyan('■', end=' ')
            elif matrix[i][j] == 2:
                print_with_yellow('■', end=' ')
            elif matrix[i][j] == 3:
                print_with_magenta('■', end=' ')
            elif matrix[i][j] == 4:
                print_with_grey('■', end=' ')
            elif matrix[i][j] == 5:
                print_with_blue('■', end=' ')
            elif matrix[i][j] == 6:
                print_with_red('■', end=' ')
            elif matrix[i][j] == 7:
                print_with_green('■', end=' ')
            elif matrix[i][j] == 8:
                print_with_white('■', end=' ')
            else:
                print(' ', end='')
        print()

# ?_______________________________________________________________

# give a size to the matrix who represent the game
n = 20 # number of lines # * le vrai tableau fait 40 lignes
p = 10 # number of columns# * le vrai tableau fait 30 colonnes

# give the touch who can use in game
left = 'q'
right = 'd'
down = 's'
rotate = 'z'

# give a time between each turn
time_between_turn = 0.5

# list of matrix who represent tetris pieces who can use in game (T, L, J, S, Z, I, O)
I = [[1, 1, 1, 1]]
O = [[2, 2], [2, 2]]
T = [[3, 3, 3], [0, 3, 0]]
L = [[4, 4, 4], [4, 0, 0]]
J = [[5, 5, 5], [0, 0, 5]]
Z = [[6, 6, 0], [0, 6, 6]]
S = [[0, 7, 7], [7, 7, 0]]

# list of colors who can use in game
invisible = (0, 0, 0)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)


# create a function that makes a matrix of zeros of size (n, p)
def make_matrix(n, p):
    return [[0 for x in range(p)] for y in range(n)]


# create a function who return a random piece
def random_piece():
    return random.choice([I, O, T, L, J, S, Z])


# create a function who return a new matrix with the piece in the coordinates (x, y)
def add_piece(matrix, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            matrix[i + y][j + x] = piece[i][j]
    return matrix


# create a function who verified if a line is full
def is_full_line(matrix, y):
    for i in range(len(matrix[y])):
        if matrix[y][i] == 0:
            return False
    return True


# create a function who delete a line
def delete_line(matrix, y):
    for i in range(y, 0, -1):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i - 1][j]
    return matrix


# create a function who delete all full lines
def delete_full_lines(matrix):
    y = 0
    while y < len(matrix):
        if is_full_line(matrix, y):
            matrix = delete_line(matrix, y)
            matrix = descend_pieces(matrix)
        else:
            y += 1
    return matrix


# create a function who verified the first line contain only zeros
def is_empty_line(matrix):
    for i in range(len(matrix[0])):
        if matrix[0][i] != 0:
            return False
    return True

# create a function who descend a piece in the matrix
def descend_piece(matrix, piece, x, y):
    if can_descend(matrix, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] != 0:
                    place_piece(matrix, piece, x, y+1)
    return matrix

# create a function who place a piece in the matrix
def place_piece(matrix, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                matrix[y + i][x + j] = piece[i][j]
    return matrix

# create a function who descend all pieces in the matrix while it is possible
def descend_pieces(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                while i < len(matrix) - 1 and matrix[i + 1][j] == 0:
                    matrix[i + 1][j] = matrix[i][j]
                    matrix[i][j] = 0
                    i += 1
    return matrix





# create a function who delete a piece (with delete_piece) in the matrix and verified if the piece can descend
def can_descend(matrix, piece, x, y):
    delete_piece(matrix, piece, x, y)
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                if y + i + 1 == len(matrix) or matrix[y + i + 1][x + j] != 0:
                    return False
    return True

# create a function who delete a piece (with delete_piece) in the matrix and verified if the piece can move to the left
def can_move_left(matrix, piece, x, y):
    delete_piece(matrix, piece, x, y)
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                if x + j - 1 < 0 or matrix[y + i][x + j - 1] != 0:
                    return False
    return True


# create a function who turn the piece in the matrix in the right direction
def turn_piece(piece):
    new_piece = []
    for i in range(len(piece[0])):
        new_piece.append([])
        for j in range(len(piece)):
            new_piece[i].append(piece[j][i])
    new_piece.reverse()
    return new_piece


# create a function who delete a piece (with delete_piece) in the matrix and verified if the piece can move to the right. if the piece don't out of the matrix and if the piece don't touch another piece
def can_move_right(matrix, piece, x, y):
    delete_piece(matrix, piece, x, y)
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                if x + j + 1 == len(matrix[0]) or matrix[y + i][x + j + 1] != 0:
                    return False
    return True


# create a function who delete a piece in the matrix
def delete_piece(matrix, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                matrix[y + i][x + j] = 0
    return matrix


# create a function who move a piece to the left
def move_left(matrix, piece, x, y):
    if can_move_left(matrix, piece, x, y):
        print("can move left")
    return matrix

# create a function who move a piece to the right. the function delete the piece in the matrix, move the piece to the right and place the piece in the matrix
def move_right(matrix, piece, x, y):
    if can_move_right(matrix, piece, x, y):
        print("can move right")
    return matrix



# !_____________________________________________________
#create a function for the movement of the piece
def move_piece(matrix, piece, x, y):
    if keyboard.is_pressed('q'):
        matrix = delete_piece(matrix, piece, x, y)
        x -= 1
    elif keyboard.is_pressed('d'):
        matrix = delete_piece(matrix, piece, x, y)
        x += 1
    elif keyboard.is_pressed('z'):
        piece = turn_piece(piece)
    elif keyboard.is_pressed('s'):
        matrix = delete_piece(matrix, piece, x, y)
        y -= 1
    return matrix, piece, x, y

# !_____________________________________________________

# create game loop
def main():
    matrix = make_matrix(n, p)
    while is_empty_line(matrix):
        matrix = delete_full_lines(matrix)
        piece_usefull = random_piece()
        x = random.randint(0, p - 4)
        y = 0
        add_piece(matrix, piece_usefull, x, y)
        while can_descend(matrix, piece_usefull, x, y):
            matrix = descend_piece(matrix, piece_usefull, x, y)
            matrix, piece_usefull, x, y = move_piece(matrix, piece_usefull, x, y)
            print_matrix(matrix)
            time.sleep(time_between_turn)
            matrix, piece_usefull, x, y = move_piece(matrix, piece_usefull, x, y)
            os.system('cls')
            y+=1
        matrix = descend_piece(matrix, piece_usefull, x, y-1)
        print_matrix(matrix)
        time.sleep(time_between_turn)
        os.system('cls')
    print_matrix(matrix)
    print("Game Over")

if __name__ == '__main__':
    main()
