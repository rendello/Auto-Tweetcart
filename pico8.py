#!/usr/bin/python3.7

""" Runs horribly insecure code through subprocess.

For use only in a secure, containerized environment!
"""

import os
import subprocess
import pyperclip
from time import sleep


def get_pico8_window(display: str) -> str:
    try:
        window_cmd = subprocess.run(f"DISPLAY=:{display} xwininfo -root -tree | grep PICO-8", shell=True, capture_output=True, check=True)
        window = window_cmd.stdout.decode("utf-8").split()[0]
    except subprocess.CalledProcessError:
        window = str()

    return window


def start_pico8(display: str) -> str:
    os.system(f"DISPLAY=:{display} pico8 -desktop ~/Desktop/Test -gif_scale 4 &")
    sleep(6)
    return get_pico8_window(display)


def kill_pico8():
    os.system("killall pico8")


def run_pico8_code(code: str, window: str, display: str) -> None:
    pyperclip.copy(code)

    # Copy clipboard to other display's clipboard
    os.system(f"xclip -selection clipboard -d $DISPLAY -o | xclip -selection clipboard -d :{display} -i")

    instructions = [
        f"DISPLAY=:{display} xdotool key --window {window} Escape",
        f"DISPLAY=:{display} xdotool key --window {window} ctrl+v",
        f"DISPLAY=:{display} xdotool key --window {window} Escape",
        f"DISPLAY=:{display} xdotool type --window {window} run",
        f"DISPLAY=:{display} xdotool key --window {window} Return",
        f"DISPLAY=:{display} xdotool key --window {window} F8",
    ]

    for i in instructions:
        print(i)
        os.system(i)
    sleep(30)
    os.system(f"DISPLAY=:{display} xdotool key --window {window} F9")


if __name__ == "__main__":
    kill_pico8()

    display = "10"
    code = "::_:: print('test', flr(rnd(150))-30,flr(rnd(140-10)),ceil(rnd(15))) flip() goto _"
    window = start_pico8(display)

    run_pico8_code(code, window, display)
