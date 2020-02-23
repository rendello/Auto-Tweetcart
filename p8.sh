#!/bin/bash

# Delete previous GIF
rm ~/atc/GIF/*

# Start virtual display
Xvfb :10 -ac -screen 0 1024x768x24 

# Start PICO-8 (and wait for intro)
DISPLAY=:10 pico8 -desktop ~/atc/GIF -gif_scale 4 &
sleep 6

# Get PICO-8 window ID
window="$(DISPLAY=:10 xwininfo -root -tree | grep PICO-8 | cut -d' ' -f6)"

# Copy code to clipboard in correct display
cat ~/atc/code | xclip -selection clipboard -d :10 -i

# Paste, run, and start recording in PICO-8
DISPLAY=:10 xdotool key --window $window Escape
DISPLAY=:10 xdotool key --window $window ctrl+v
DISPLAY=:10 xdotool key --window $window Escape
DISPLAY=:10 xdotool type --window $window run
DISPLAY=:10 xdotool key --window $window Return
DISPLAY=:10 xdotool key --window $window F8

# Stop recording after 30 seconds
sleep 30
DISPLAY=:10 xdotool key --window $window F9

# Teardown (keep GIF for extraction)
sleep 10
killall pico8
rm ~/atc/code

# Optimize GIF (it's huge so it might not fit under limit)
gifsicle ~/atc/GIF/PICO-8_0.gif --optimize=3 --output ~/atc/GIF/PICO-opti.gif
