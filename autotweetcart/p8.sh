#!/bin/bash

# -- Important if PICO8 wasn't closed correctly
killall --quiet pico8

# -- Delete previous GIF
rm ~/atc/GIF/*

# -- Start PICO-8 (and wait for intro)
DISPLAY=:10 ~/pico8 -desktop ~/atc/GIF -gif_scale 4 -gif_len 120 &
sleep 5

# -- Get PICO-8 window ID
window="$(DISPLAY=:10 xwininfo -root -tree | grep PICO-8 | cut -d' ' -f6)"

# -- Copy code to clipboard in correct display
cat ~/atc/code | xclip -selection clipboard -d :10 -i

# -- Paste, run, and start recording in PICO-8
DISPLAY=:10 xdotool key --window $window Escape
sleep .1
DISPLAY=:10 xdotool key --window $window ctrl+v
DISPLAY=:10 xdotool key --window $window ctrl+r
DISPLAY=:10 xdotool key --window $window F8

# -- Stop recording after 30 seconds
sleep 30
DISPLAY=:10 xdotool key --window $window F9

# -- Teardown (keep GIF for extraction)
sleep 10
killall pico8
rm ~/atc/code

gif_path=~/atc/GIF/PICO-opti.gif

# -- Optimize GIF (it's huge so it might not fit under limit otherwise)
gifsicle ~/atc/GIF/PICO-8_0.gif --optimize=3 --output $gif_path

size=$(du -b $gif_path | cut -d$'\t' -f1)
framecount=$(exiftool -b -FrameCount $gif_path)

# If the frame count is an empty string, the GIF has been broken by
# Gifsicle. This occurs occasionally with GIFs that have no changes (ie.
# should be shrunk to a single frame). Uses unoptimized GIF instead.
if [[ -z $framecount ]]; then
	echo GIF Broken, using unoptimized version.
	cp ~/atc/GIF/PICO-8_0.gif $gif_path
fi

# -- If GIF is still too big, cut its frame number down until it's not
while (( $size > 15000000 )); do
	framecount=$(exiftool -b -FrameCount $gif_path)
	echo $framecount $size

	if (( framecount > 200 )); then
		sub_no=$((100))
	elif (( framecount > 10 )); then
		sub_no=$((10))
	else
		sub_no=$((1))
	fi

	gifsicle $gif_path '#0-'$(($framecount-$sub_no))'' -o $gif_path
	size=$(du -b $gif_path | cut -d$'\t' -f1)
done
