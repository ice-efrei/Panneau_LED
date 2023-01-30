from time import sleep
from typing import List, Tuple
import os

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

FPS = 24

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)

example = [
    [R, R, R, R, R],
    [R, R, B, R, R],
    [R, G, B, G, R],
    [R, R, B, R, R],
    [R, R, R, R, R],
]


# ------------------------------
# Only on raspberry pi
# ------------------------------
# from board import D18
# from neopixel import NeoPixel, ORDER


# pixel_pin = D18
# num_pixels = 1200
# led_strip = NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)


# def display_on_leds (array: List[List[Tuple[int]]], leds: NeoPixel) -> None:
#     """
#     Display the array on the LED strip
#     :param array: array to display
#     :return: None
#     """
#     for y in range(len(array)):
#         for x in range(len(array[y])):
#             leds[XY(x, y, len(array[y]), len(array))] = array[y][x]
#     leds.show()


# ------------------------------
# End of raspberry pi only code
# ------------------------------

def XY (x: int, y: int, w: int, h: int ) -> int:
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
    

def display_on_console (array: List[List[Tuple[int]]]) -> None:
    """
    Display the array on the bash terminal with colors and █ characters
    :param array: array to display
    :return: None
    """
    for y in range(len(array)):
        for x in range(len(array[y])):
            print(f"\033[48;2;{array[y][x][0]};{array[y][x][1]};{array[y][x][2]}m  ", end="")
        print("\033[0m")


def main():
    try:
        while True:
            clear()
            # display_on_leds(example, led_strip)
            display_on_console(example)
            sleep(1/FPS)
            # input()  #  step by step
            example.insert(0, example.pop())  #  push the last line to the first line
    except KeyboardInterrupt:
        # led_strip.fill((0, 0, 0))
        # led_strip.show()
        print("Bye!")

if __name__ == "__main__":
    main()