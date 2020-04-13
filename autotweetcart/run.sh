#!/bin/bash

rm ./GIF/*

# -- Start virtual display (if not already started)
if [[ -z $(pgrep Xvfb) ]]; then
	lxc exec p8 -- Xvfb :10 -ac -screen 0 1024x768x24 &
fi

lxc file push code_file p8/root/atc/code
lxc exec p8 -- ~/atc/p8.sh
lxc file pull p8/root/atc/GIF/PICO-opti.gif ./GIF/
