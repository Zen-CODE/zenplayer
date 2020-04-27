"""
This module provices a wrapper for the Kivy Soundload class. It inject the
SoundVLCPlayer as the default audio provider.
"""
from .audio_vlc import SoundVLCPlayer
from kivy.core.audio import SoundLoader
from os import environ


def register_vlc():
    """
    Register the SoundVLCPlayer as the default audio player for the Kivy
    Sounloader class
    """
    SoundLoader.register(SoundVLCPlayer)
    environ["KIVY_AUDIO"] = "vlcplayer"


register_vlc()
