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

    def on_enter(self):
        super().on_enter()

        lib = self.ctrl.library
        self.ids.image.source = lib.get_album_cover(
            self.artist, self.album)
        self.ids.rv.data = [
            {"text": item} for item in lib.get_tracks(self.artist,
                                                      self.album)]
