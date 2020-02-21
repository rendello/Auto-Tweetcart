#!/usr/bin/python3.7

""" Runs horribly insecure code through subprocess.

For use only in a secure, containerized environment!
"""

import subprocess
import pyperclip
from time import sleep

def run_pico8_code(code: str, window: str) -> bool:
    pyperclip.copy(code)

    instructions = [
        f"xdotool key --window {window} Escape",
        f"xdotool key --window {window} ctrl+v",
        f"xdotool key --window {window} Escape",
        f"xdotool type --window {window} run",
        f"xdotool key --window {window} Return",
        f"xdotool key --window {window} F8",
    ]

    for i in instructions:
        print(i)
        subprocess.run(i.split())
    sleep(3)
    subprocess.run(f"xdotool key --window {window} F9".split())


e = """
cls(1)c,s,b,g,d=circfill,64,37,24576,104::_::for i=1,128 do
x,y=rnd(128),rnd(90)
if(pget(x,y)==8)pset(x,y+rnd(3),8)pset(x,y-1,1)end
c(s,b,32,8)c(d,d,b,0)c(s,d,20,0)memset(g+91*s,0,b*s)
?"웃웃",97,62,0
?"웃",61,47,0
for i=0,b,2 do 
memcpy(g+(i+90)*s,g+(90-i*2)*s,s)end
flip()goto _
"""

e = """
z=128w=64g,h=line,circfill::_::cls()
if(t()%8<rnd(.3))cls(7)
for n=66,84,8 do
s={}for x=-1,z do
i=rnd(z)g(x,i,x+5,i-9,1)a=12l=.0002y=n
for n=1,4 do 
y+=sin(x*l+t()*n*.1)*a
l*=3a/=.9end
g(x,m,x,z)s[x+1]=y+6m=y end
if n==66 then
k=s[61]h(w,k,4,14)h(66,k-2,.5,7)
end end flip()goto _
"""
