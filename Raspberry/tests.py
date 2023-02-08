from time import sleep

from pynput import keyboard

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
        print("up")
    elif key == keyboard.Key.down:
        print("down")
    elif key == keyboard.Key.left:
        print("left")
    elif key == keyboard.Key.right:
        print("right")
    else:
        print("other")


def on_release(key):
    if key == keyboard.Key.up:
        print("up")
    elif key == keyboard.Key.down:
        print("down")
    elif key == keyboard.Key.left:
        print("left")
    elif key == keyboard.Key.right:
        print("right")
    else:
        print("other")


# Collect events until released
listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
listener.start()

while True:
    sleep(1 / 10)
    print("Hello World")
