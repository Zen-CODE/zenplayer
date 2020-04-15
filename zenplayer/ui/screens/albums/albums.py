"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty
from ui.widgets.zenrecycleview import SelectableLabel
from kivy.clock import Clock
from ui.widgets.zenrecycleview import SelectableLabel
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

    def add_to_playlist(self, replace=False):
        """
        Add the selected album to the playlist
        """
        pl = self.ctrl.playlist
        if replace:
            pl.clear_files()
        album_path = self.ctrl.library.get_path(self.artist, self.album)
        pl.add_files(album_path)
        if replace:
            self.ctrl.play_index(0)

    def choose_random(self):
        """ Choose and display a randbom album. """
        self.artist, self.album = self.ctrl.library.get_random_album()

    def item_touched(self, item):
        """ Show the popup for selecting the album """
        AlbumPopup(
            title="Track: {self.artist} - {self.album}",
            handler=self).open()


class AlbumPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    handler = ObjectProperty()
    """ A reference to the controller object"""
