#!/usr/bin/python3.7

import re

def extract_code(text: str, tokens: list) -> str:
    """ Extracts code from text by comparing tokens.

    More specifically, it reads in text line-by-line, and gives it a score based
    on how code-like it is. The positive tokens, being common tokens from the
    programming language, will add points. Negative tokens, such as hashtags,
    will remove points.

    If the starting and / or ending lines are especially un-codelike, they will
    be stripped.

    Args:
        text: The text (usually from a tweet) to be passed.
        tokens: list of dicts in the format <token>: <score>
    """

    line_scores = []
    for line in text.split("\n"):
        score = 0

        # If it's a comment, it can be ignored and thrown away
        if line.startswith("--") or line.startswith("//") or line.startswith("#"):
            score = -100
        else:
            # Pico-8 print alias
            if line.startswith("?"):
                score += 5
            splits = []
            splits.extend(re.findall(r"[\w']+", line))
            splits.extend(re.findall(r"[\W']+", line))
            for word in splits:
                try:
                    score += tokens[word]
                except KeyError:
                    pass
        line_scores.append(score)

    return line_scores


probably_not_lua = [
    "tweetcart",
    "tweetjam",
    "pico8",
]

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
    "-",
    "music",
    "map",
    "camera",
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
]

almost_certainly_lua = [
    "nil",
    "elseif",
    "goto",
    "::_::",
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
    "-",
    "~",
    "^",
]

tokens = {}
tokens.update({token: -10 for token in probably_not_lua})
tokens.update({token: 1 for token in maybe_lua})
tokens.update({token: 3 for token in likely_lua})
tokens.update({token: 5 for token in almost_certainly_lua})

e ="""
t=0::f::s=sin(t)
memcpy(24456+s*2,
24316+s*4+t*2,8192)
t+=.02flip()goto f

My attempt at leanest and meanest #tweetcart 

Loses information over time

#pico8
"""
print(extract_code(e, tokens))
