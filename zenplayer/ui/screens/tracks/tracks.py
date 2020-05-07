"""
This module houses the screen displaying a tracks listing for an album
"""
from kivy.properties import StringProperty
from ui.screens.zenscreen import ZenScreen
from kivy.clock import Clock

class TracksScreen(ZenScreen):
    """
    The main screen that shows whats currently playing
    """
    artist = StringProperty()

    album = StringProperty()

    def on_leave(self):
        super().on_leave()
        self.artist = self.album = ""  # Force reload of data

    def on_album(self, _widget, value):
        if value and self.artist:
            Clock.schedule_once(lambda dt: self.load())

    def on_artist(self, _widget, value):
        if value and self.album:
            Clock.schedule_once(lambda dt: self.load())

    def load(self):
        """ Load the tracks for the given artist and album """
        lib = self.ctrl.library
        self.ids.image.source = lib.get_album_cover(
            self.artist, self.album)
        self.ids.rv.data = [
            {"text": item} for item in lib.get_tracks(self.artist,
                                                      self.album)]
