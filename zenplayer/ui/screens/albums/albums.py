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
        self.ctrl.show_screen("Artists", artist=text)
