"""
This module houses the Zen Music Library browser based on the recycleview
"""
from ui.screens.zenscreen import ZenScreen


class ArtistsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.ids.rv.data = [
            {"text": artist} for artist in self.ctrl.library.get_artists()]
