#!/usr/bin/python3.7

""" Runs horribly insecure code through subprocess.

For use only in a secure, containerized environment!
"""

import subprocess


def intercept_restricted_tokens(text):
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
    restricted_tokens = [
        "cstore",
        "reload",
        "printh"
    ]
    for token in restricted_tokens:
        if token in text:
            return no_io
    return text


