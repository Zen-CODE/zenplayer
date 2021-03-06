"""
This module houses the Artist display UI
"""
from ui.screens.zenscreen import ZenScreen
from ui.widgets.zenkeydown import ZenKeyDown


class ArtistsScreen(ZenKeyDown, ZenScreen):
    """
    Displays a interface for viewing and interacting with the artists
    list from the library.
    """
    def on_enter(self):
        """ Handle the on enter event """
        super().on_enter()
        if not self.ids.rv.data:
            self.ids.rv.data = [
                {"text": artist} for artist in self.ctrl.library.get_artists()]

    def item_touched(self, label):
        """
        The label has been clicked of enter pressed with it selected.
        """
        self.ctrl.zenplayer.show_screen(
            "Albums", artist=label.text, album="")
