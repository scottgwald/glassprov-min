#! /bin/bash

# clear off existing scripts
adb shell rm -r /sdcard/wearscript/gists/*

# install this script
adb shell mkdir /sdcard/wearscript/gists/glassprov
adb push b612c849601a8de2ecae /sdcard/wearscript/gists/glassprov

# set endpoint
# setendpoint.sh
