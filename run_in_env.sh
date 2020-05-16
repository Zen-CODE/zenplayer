#!/bin/bash
echo "Changing to the ZenPlayer folder and launching."
cd "${0%/*}"
. venv/bin/activate
KIVY_AUDIO=vlcplayer python zenplayer/main.py