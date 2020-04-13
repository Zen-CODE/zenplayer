"""
This module houses the Artist display UI
"""
from ui.screens.zenscreen import ZenScreen


class ArtistsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the artists
    list from the library.
    """
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.ids.rv.data = [
            {"text": artist} for artist in self.ctrl.library.get_artists()]

    def on_selected(self, index, text):
        """
        An label with the given text has been selected from the recycleview.
        """
        self.ctrl.show_screen("Albums", artist=text)
