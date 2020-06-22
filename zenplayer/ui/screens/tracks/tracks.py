"""
This module houses the screen displaying a tracks listing for an album
"""
from kivy.properties import StringProperty
from ui.screens.zenscreen import ZenScreen
from kivy.clock import Clock
from os.path import join


class TracksScreen(ZenScreen):
    """
    The main screen that shows whats currently playing
    """
    artist = StringProperty()

    album = StringProperty()

    track = ""

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

    def item_touched(self, item):
        """ Show the context for selecting the album """
        self.track = item.text
        self.ctrl.zenplayer.show_screen(
            "Context", title=f"Track: {self.track}",
            parent_screen="Tracks",
            actions=[
                {"text": "Add to playlist",
                 "action": self.add_to_playlist},
                {"text": "Play next",
                 "action": lambda: self.add_to_playlist(mode="next")},
                {"text": "Play now (insert)",
                 "action": lambda: self.add_to_playlist(mode="insert")},
                {"text": "Play now (replace)",
                 "action": lambda: self.add_to_playlist(mode="replace")},
                {"text": "Cancel",
                 "action": lambda: None}
            ])

    def add_to_playlist(self, mode="add"):
        """
        Add the selected album to the playlist. *mode* can be one of
        * "add" - add to the end of the playlist
        * "replace" - clear the existing playlist and add the files
        * "insert" - insert the selected album at the beginning of the playlist
        """
        album_path = self.ctrl.library.get_path(self.artist, self.album)
        self.ctrl.playlist.add_files(join(album_path, self.track), mode=mode)
        if mode in ["replace", "insert"]:
            self.ctrl.play_index(0)

