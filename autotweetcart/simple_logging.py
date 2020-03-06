#!/usr/bin/python3.7

from pathlib import Path
from time import localtime, strftime

def log(message, restrict=True):
    if restrict:
        # Truncate message.
        message = (message[:75] + '…') if len(message) > 75 else message
        message = message.replace("\n", " ")

    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime())
    log_message = f"[{time_str}] {message}"
    print(log_message)
    with open(log_file, "a+") as f:
        f.write(log_message + "\n")

log_file = Path("~/.autotweetcart/log.txt").expanduser()
