"""
This module houses the Artist display UI
"""
from ui.screens.zenscreen import ZenScreen


class ArtistsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the artists
    list from the library.
    """

    def on_enter(self):
        """
        As the loading can sometimes take time, do this once the screen is
        shown.
        """
        if not self.ids.rv.data:
            self.ids.rv.data = [
                {"text": artist} for artist in self.ctrl.library.get_artists()]
            lbl = self.ids.wait_label
            lbl.parent.remove_widget(lbl)

    def item_selected(self, label):
        """
        An label with the given text has been selected from the recycleview.
        """
        self.ctrl.show_screen("Albums", artist=label.text)
