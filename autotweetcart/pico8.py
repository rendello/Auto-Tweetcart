#!/usr/bin/python3.7

import subprocess


def remove_bot_call(text):
    new_text = ""
    for line in text.split("\n"):
        if "@auto_tweetcart" not in line:
            new_text += f"{line}\n"
    return new_text


def has_bad_words(text, profanity_file_path) -> bool:
    with open(profanity_file_path, "r") as f:
        for line in f.readlines():
            if line.strip("\n") in text:
                return True
    return False


def intercept_restricted_tokens(text) -> str:
    no_io = """
    function middle_print(text, y)
        print(text, 64-((4*#text)/2), y, 7)
    end
    pixels = {}
    for i=0, 100 do
        pixels[i] = {flr(rnd(128)), flr(rnd(128)), 9}
    end
    cls()
    function _draw()
        for _, p in pairs(pixels) do
            if p[1] > 128 or p[2] > 128 then
                p[1] = -10-flr(rnd(90))
                p[2] = -10-flr(rnd(90))
                p[3] += 1
                if p[3] == 17 then
                        p[3] = 0
                end
            end
            p[1] += -1 + ceil(rnd(2))
            p[2] += -1 + ceil(rnd(2))
            pset(p[1], p[2], p[3])
        end

        rectfill(20, 37, 106, 68, 0)
        middle_print("commands that can do", 45)
        middle_print("file i/o not allowed", 55)
    end
    """
    restricted_tokens = ["cstore", "reload", "printh"]
    for token in restricted_tokens:
        if token in text:
            return no_io
    return text


def process_code(text):
    if has_bad_words(text, "profanity.txt"):
        return False

    text = remove_bot_call(text)
    text = intercept_restricted_tokens(text)
    with open("code_file", "w") as f:
        f.write(text)
    
    subprocess.run("./run.sh")
    return True
