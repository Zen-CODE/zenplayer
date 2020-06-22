"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from ui.widgets.zenkeydown import ZenKeyDown
from ui.widgets.zenpopup import ZenPopup
from random import choice


class AlbumsScreen(ZenKeyDown, ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    artist = StringProperty()
    """ The artist for which to display the ALbum """

    album = StringProperty("")
    """ The album that has been selected. """

    randomise = BooleanProperty(False)
    """ Set to True to seleact a random album """

    def on_artist(self, _widget, artist):
        """ Respond to the changing of artists"""
        def update(_dt):
            albums = self.ctrl.library.get_albums(artist)
            self.ids.rv.data = [
                {"text": album} for album in albums]
            if not self.album:
                self.album = choice(albums)

            self.ids.rv.find_item(self.album)
        Clock.schedule_once(update)

    def item_selected(self, label, selected):
        """
        An item (SelectableLabel) has been selected from the recycleview.
        """
        if selected:
            self.album = label.text

    def add_to_playlist(self, mode="add"):
        """
        Add the selected album to the playlist. *mode* can be one of
        * "add" - add to the end of the playlist
        * "replace" - clear the existing playlist and add the files
        * "insert" - insert the selected album at the beginning of the playlist
        """
        self.ctrl.playlist.add_files(
            self.ctrl.library.get_path(self.artist, self.album), mode=mode)
        if mode in ["replace", "insert"]:
            self.ctrl.play_index(0)

    def on_randomise(self, _widget, value):
        """ Choose and display a randbom album. """
        if value:
            # Set the album before the artist to prevent reset on loading
            self.artist, self.album = self.ctrl.library.get_random_album()
            self.randomise = False

    def item_touched(self, item):
        """ Show the popup for selecting the album """
        # AlbumPopup(
        #     title=f"Album: {self.artist} - {self.album}",
        #     handler=self).open()

        self.ctrl.zenplayer.show_screen(
            "Context", title=f"Album: {self.artist} - {self.album}",
            actions=[
                {"text": "Add to playlist",
                 "action": self.add_to_playlist},
                {"text": "Play next",
                 "action": lambda: self.add_to_playlist(mode="next")},
                {"text": "Play now (insert)",
                 "action": lambda: self.add_to_playlist(mode="insert")},
                {"text": "Play now (replace)",
                 "action": lambda: self.add_to_playlist(mode="replace")},
                {"text": "View Tracks",
                 "action": lambda dt: self.view_tracks()},
                {"text": "Cancel",
                 "action": lambda: self.ctrl.zenplayer.show_screen(
                     "Albums", artist=self.artist, album=self.album)}
            ])

    def view_tracks(self):
        """ Show a detailed track listing for this album """
        self.ctrl.zenplayer.show_screen("Tracks", artist=self.artist,
                                        album=self.album)


class AlbumPopup(ZenPopup):
    """
    The Popup show when the playlist item is tapped and held.
    """
