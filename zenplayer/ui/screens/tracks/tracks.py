"""
This module houses the screen displaying a tracks listing for an album
"""
from kivy.properties import StringProperty
from ui.screens.zenscreen import ZenScreen


class TracksScreen(ZenScreen):
    """
    The main screen that shows whats currently playing
    """
    artist = StringProperty()

    album = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
