#!/bin/bash
echo "Changing to the ZenPlayer folder and launching."
. venv/bin/activate
KIVY_AUDIO=vlcplayer python zenplayer/main.py
