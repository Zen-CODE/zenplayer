#!/bin/bash
cd "${0%/*}"
sudo env KIVY_AUDIO=vlcplayer venv/bin/python zenplayer/main.py