#! /bin/bash

# clear off existing scripts
adb shell rm -r /sdcard/wearscript/gists/*

# install this script
adb shell mkdir /sdcard/wearscript/gists/glassprov
adb push 4fd78440330c45376aa0 /sdcard/wearscript/gists/glassprov

# set endpoint
# setendpoint.sh
