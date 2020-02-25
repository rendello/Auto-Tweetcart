#!/bin/bash

rm ./GIF/*

lxc file push code_file p8/root/atc/code
lxc exec p8 -- ~/atc/p8.sh
lxc file pull p8/root/atc/GIF/PICO-opti.gif ./GIF/
