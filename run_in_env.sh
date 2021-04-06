#!/bin/bash
echo "Changing to the ZenPlayer folder and launching."
KIVY_AUDIO=vlcplayer LD_PRELOAD=./zenplayer/libLeap.so python zenplayer/main.py
