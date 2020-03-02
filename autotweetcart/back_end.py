#!/usr/bin/python3.7

import subprocess
import base64


def has_bad_words(text, profanity_file_path) -> bool:
    """ Returns True if there are bad words.

    Bad words are base64 encoded as I don't want to host every swear, slur and
    rude phrase in cleartext on my Gitlab.
    """
    with open(profanity_file_path, "r") as f:
        curses = base64.b64decode(f.read()).decode("utf-8")
        for curse in curses.split("\n"):
            if curse in text.lower():
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


def process_code(text: str) -> dict:
    """ Processes & runs PICO-8 code.

    Args:
        text: The extracted text from the Tweet, call to bot removed.

    Returns:
        (dict):
            was_successful: If code was run.
            title: The title of the Tweetcart as extracted from the code.
    """
    failure = {"was_successful": False, "title": None}

    if has_bad_words(text, "profanity.txt"):
        return failure

    if not is_lua(text):
        return failure

    text = intercept_restricted_tokens(text)

    title = grab_title(text)

    with open("code_file", "w") as f:
        f.write(text)

    subprocess.run("./run.sh")
    return {"was_successful": True, "title": title}


def grab_title(text):
    for line in text.split("\n"):
        for comment_denoter in ("--", "//"):
            if line.startswith(comment_denoter):
                potential = line.replace("--", "").strip()
                if potential != "":
                    return potential
    return None


def is_lua(text) -> bool:

    maybe_lua = [
        "if",
        "while",
        "do",
        "then",
        "and",
        "not",
        "for",
        "end",
        "in",
        "or",
        "else",
        "until",
        "time",
        "type",
        ";",
        "sin",
        "trace",
        "add",
        "all",
        "&",
        "+",
        "music",
        "map",
        "camera",
        "(",
        ")",
    ]

    likely_lua = [
        "repeat",
        "local",
        "function",
        "break",
        "return",
        "false",
        "true",
        "function",
        "clip",
        "sfx",
        "print",
        "nil",
        "elseif",
        "goto",
        "::",
        "circ",
        "circfill",
        "cls",
        "color",
        "cursor",
        "fget",
        "fillp",
        "fset",
        "line",
        "pal",
        "palt",
        "pget",
        "pset",
        "rect",
        "rectfill",
        "sget",
        "spr",
        "sset",
        "sspr",
        "flip",
        "_init",
        "_update",
        "_draw",
        "del",
        "foreach",
        "pairs",
        "btn",
        "btnp",
        "mget",
        "mset",
        "cstore",
        "memcpy",
        "memset",
        "peek",
        "poke",
        "reload",
        "abs",
        "atan2",
        "band",
        "bnot",
        "bor",
        "bxor",
        "cos",
        "flr",
        "max",
        "mid",
        "min",
        "rnd",
        "shl",
        "shr",
        "sqrt",
        "srand",
        "cartdata",
        "dget",
        "dset",
        "cocreate",
        "coresume",
        "costatus",
        "yield",
        "setmetatable",
        "getmetatable",
        "sub",
        "tonum",
        "tostr",
        "menuitem",
        "extcmd",
        "assert",
        "printh",
        "stat",
        "stop",
        "=",
        "{",
        "}",
        "=",
        "~=",
        "==",
        "<=",
        ">=",
        "<",
        ">",
        "|",
        "~",
        "<<",
        ">>",
        "..",
        "*",
        "/",
        "%",
        "~",
        "^",
        "--",
    ]

    score = 0
    threshold = 4
    for token in maybe_lua:
        if token in text:
            score += 1

    for token in likely_lua:
        if token in text:
            score += 3

    if score > threshold:
        return True
    return False
