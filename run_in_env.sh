#!/bin/bash
echo "Changing to the ZenPlayer folder and launching."
echo "sudo is needed for hotkey support"
echo "================================="
cd "${0%/*}"
KIVY_AUDIO=vlcplayer venv/bin/python zenplayer/main.py