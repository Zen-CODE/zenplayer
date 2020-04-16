"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class AlbumsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    artist = StringProperty()
    """ The artist for which to display the ALbum """

    album = StringProperty("")
    """ The album that has been selected. """

    def on_artist(self, _widget, artist):
        """ Respond to the changing of artists"""
        def update(_dt):
            self.ids.rv.data = [
                {"text": album} for album in self.ctrl.library.get_albums(
                    artist)]
        Clock.schedule_once(update)

    def item_selected(self, label):
        """
        An item (SelectableLabel) has been selected from the recycleview.
        """
        self.album = label.text

    def add_to_playlist(self, mode="add"):
        """
        Add the selected album to the playlist. *mode* can be one of
        * "add" - add to the end of the playlist
        * "replace" - clear the existing playlist and add the files
        * "insert" - insert the selected album at the beginning of the playlist
        """
        pl = self.ctrl.playlist
        if mode == "replace":
            pl.clear_files()

        pl.add_files(self.ctrl.library.get_path(self.artist, self.album),
                     mode=mode)
        if mode != "add":
            self.ctrl.play_index(0)

    def choose_random(self):
        """ Choose and display a randbom album. """
        self.artist, self.album = self.ctrl.library.get_random_album()

    def search(self):
        """ Search for any album or artist that contains a match. """
        ret = self.ctrl.library.search(self.ids.text.text)
        if ret:
            self.artist, self.album = ret["artist"], ret["album"]

    def item_touched(self, item):
        """ Show the popup for selecting the album """
        AlbumPopup(
            title=f"Track: {self.artist} - {self.album}",
            handler=self).open()

    def item_draw(self, label):
        """ Set the back color of the label considering the playlist """
        if label.text == self.album:
            label.back_color = [.5, 1.0, .50, .3]
            return True
        return False


class AlbumPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    handler = ObjectProperty()
    """ A reference to the controller object"""
