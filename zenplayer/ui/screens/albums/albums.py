"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty
from ui.widgets.zenrecycleview import SelectableLabel
from kivy.clock import Clock


class AlbumsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    artist = StringProperty()
    """ The artist for which to display the ALbum """

    album = StringProperty()
    """ The album that has been selected. """

    def on_artist(self, _widget, artist):
        """ Respond to the changing of artists"""
        def update(_dt):
            self.ids.rv.data = [
                {"text": album} for album in self.ctrl.library.get_albums(
                    artist)]
        Clock.schedule_once(update)

    def on_selected(self, index, text):
        """
        An label with the given text has been selected from the recycleview.
        """
        self.album = text

    def add_to_playlist(self, replace=False):
        """
        Add the selected album to the playlist
        """
        if self.album:
            album_path = self.ctrl.library.get_path(self.artist, self.album)
            self.ctrl.playlist.add_files(album_path, replace)

    def choose_random(self):
        """ Choose and display a randbom album. """
        self.artist, self.album = self.ctrl.library.get_random_album()
