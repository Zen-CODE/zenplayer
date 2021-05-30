"""This module provices a wrapper for the Kivy Soundload class.

It inject theSound VLCPlayer as the default audio provider.
"""
from kivy.core.audio import SoundLoader

from .audio_vlc import SoundVLCPlayer


def register_vlc():
    """Register the SoundVLCPlayer as the default audio player.

    This applies to the Kivy SoundLoader class. To set as the default"

        from os import environ
        environ["KIVY_AUDIO"] = "vlcplayer"

    Other options include:

        ffpyplayer, sdl2 and gstplayer
    """
    SoundLoader.register(SoundVLCPlayer)
