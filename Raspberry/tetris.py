import os
from threading import Thread

from random import choice

from inputs import get_gamepad, devices
from keyboard import hook, KEY_DOWN, KEY_UP
from time import sleep

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
random_piece = lambda: choice([I, O, T, L, J, S, Z])
is_line_full = lambda matrix, y: all(matrix[y])
is_first_line_empty = lambda matrix: all([x == 0 for x in matrix[0]])

# give a size to the matrix who represent the game
n = 20  # number of lines # * le vrai tableau fait 40 lignes
p = 15  # number of columns# * le vrai tableau fait 30 colonnes

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


def on_key_press(key):
    print("key pressed", key.name, "")
    if key.name == "up":
        arrow_keys["KEY_UP"]["state"] = True
    elif key.name == "down":
        arrow_keys["KEY_DOWN"]["state"] = True
    elif key.name == "left":
        arrow_keys["KEY_LEFT"]["state"] = True
    elif key.name == "right":
        arrow_keys["KEY_RIGHT"]["state"] = True
    else:
        pass


def on_key_release(key):
    print("key released", key.name, "")
    if key.name == "up":
        arrow_keys["KEY_UP"]["state"] = False
    elif key.name == "down":
        arrow_keys["KEY_DOWN"]["state"] = False
    elif key.name == "left":
        arrow_keys["KEY_LEFT"]["state"] = False
    elif key.name == "right":
        arrow_keys["KEY_RIGHT"]["state"] = False
    else:
        pass


# Collect events until released
def on_action(event):
    if event.event_type == KEY_DOWN:
        on_key_press(event)

    elif event.event_type == KEY_UP:
        on_key_release(event)


# Collect events until released
hook(lambda e: on_action(e))


def display_on_console(array):
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


# ------------------------------
# Only on raspberry pi
# ------------------------------

# from board import D18
# from neopixel import NeoPixel, ORDER
#
#
# pixel_pin = D18
# num_pixels = 1200
# led_strip = NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)
#
#
# def display_on_leds (array: List[List[int]], leds: NeoPixel) -> None:
#     """
#     Display the array on the LED strip
#     :param array: array to display
#     :return: None
#     """
#     for y in range(len(array)):
#         for x in range(len(array[y])):
#             for i in range(2):
#                 for j in range(2):
#                     leds[XY(x * 2 + i, y * 2 + j, p * 2, n * 2)] = colors[array[y][x]]
#     leds.show()


# ------------------------------
# End of raspberry pi only code
# ------------------------------

def XY(x: int, y: int, w: int, h: int) -> int:
    """
    Convert x,y coordinates to a single integer
    :param x: x coordinate
    :param y: y coordinate
    :param w: width of the array
    :param h: height of the array
    :return: single integer
    """
    if y % 2 == 0:
        return y * w + x
    else:
        return (y + 1) * w - x - 1


class XboxController(object):
    MAX_TRIG_VAL = pow(2, 8)
    MAX_JOY_VAL = pow(2, 15)

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X  # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state  # previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state  # previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

            if self.A == 1:
                arrow_keys["KEY_UP"]["state"] = True
            else:
                arrow_keys["KEY_UP"]["state"] = False

            if self.LeftJoystickX < -0.5:
                arrow_keys["KEY_RIGHT"]["state"] = True
            else:
                arrow_keys["KEY_RIGHT"]["state"] = False

            if self.LeftJoystickX > 0.5:
                arrow_keys["KEY_LEFT"]["state"] = True
            else:
                arrow_keys["KEY_LEFT"]["state"] = False

            if self.LeftJoystickY < -0.5:
                arrow_keys["KEY_DOWN"]["state"] = True
            else:
                arrow_keys["KEY_DOWN"]["state"] = False

            if self.LeftDPad == 1:
                arrow_keys["KEY_LEFT"]["state"] = True
            else:
                arrow_keys["KEY_LEFT"]["state"] = False

            if self.RightDPad == 1:
                arrow_keys["KEY_RIGHT"]["state"] = True
            else:
                arrow_keys["KEY_RIGHT"]["state"] = False


def main():
    matrix = [[0 for _ in range(p)] for _ in range(n)]

    current_tetrominos = random_piece()
    x = int(p / 2)
    y = 0

    continued = False

    print("*--------------*")
    print("| Tretris Game |")
    print("*--------------*")

    if devices.gamepads:
        joy = XboxController()
    else:
        joy = None

    while is_first_line_empty(matrix):
        if not can_descend(matrix, current_tetrominos, x, y):
            # if the tetrominos cannot go down then we check for any full line to score then we create a new tetrominos
            matrix = delete_full_lines(matrix)
            current_tetrominos = random_piece()
            x = int(p / 2)  # randint(0, p - 4)
            y = 0
            if continued:
                break
            continued = True
            continue

        if joy is not None:
            jx, jy, a, b, rb = joy.read()

            if jx < -0.5:
                arrow_keys["KEY_LEFT"]["state"] = True
            else:
                arrow_keys["KEY_LEFT"]["state"] = False

            if jx > 0.5:
                arrow_keys["KEY_RIGHT"]["state"] = True
            else:
                arrow_keys["KEY_RIGHT"]["state"] = False

            if jy < -0.5:
                arrow_keys["KEY_DOWN"]["state"] = True
            else:
                arrow_keys["KEY_DOWN"]["state"] = False

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
        # display_on_leds(matrix, led_strip)
        sleep(1 / frame_per_seconds)
        clear()
    display_on_console(matrix)
    print("Game Over")


if __name__ == '__main__':
    while True:
        main()
        sleep(3)
