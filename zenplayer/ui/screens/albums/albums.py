"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from ui.widgets.zenkeydown import ZenKeyDown


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

    chosen = StringProperty("")
    """ The last album selected via randomize """

    def on_artist(self, _widget, artist):
        """ Respond to the changing of artists"""
        def update(_dt):
            self.ids.rv.data = [
                {"text": album} for album in self.ctrl.library.get_albums(
                    artist)]
            self.ids.rv.find_item(self.album)
        Clock.schedule_once(update)

    def item_selected(self, label, selected):
        """
        An item (SelectableLabel) has been selected from the recycleview.
        """
        self.album = label.text if selected else self.chosen

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
            _artist, self.chosen = self.ctrl.library.get_random_album()
            self.album = self.chosen
            self.artist = _artist
            self.randomise = False

    def item_touched(self, item):
        """ Show the popup for selecting the album """
        AlbumPopup(
            title=f"Track: {self.artist} - {self.album}",
            handler=self).open()

    def item_draw(self, label):
        """ Set the back color of the label considering the playlist """
        if label.text == self.chosen:
            label.back_color = [.5, 1.0, .50, .3]
            return True
        return False


class AlbumPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    handler = ObjectProperty()
    """ A reference to the controller object"""
