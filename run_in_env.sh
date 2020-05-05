#!/bin/bash
echo "Changing to the ZenPlayer folder and launching."
cd "${0%/*}"
KIVY_AUDIO=vlcplayer venv/bin/python zenplayer/main.py