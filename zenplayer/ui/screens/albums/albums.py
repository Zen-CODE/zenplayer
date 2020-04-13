"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty
from ui.widgets.zenrecycleview import SelectableLabel


class AlbumsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    artist = StringProperty()
    """ The artist for which to display the ALbum """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.ids.rv.data = [
            {"text": artist} for artist in self.ctrl.library.get_artists()]

    def on_selected(self, index, text):
        """
        An label with the given text has been selected from the recycleview.
        """
        self.ctrl.show_screen("Artists", artist=text)
