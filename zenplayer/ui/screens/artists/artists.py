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
        self.ctrl.kb_handler.add_callback(self.ids.rv.on_key_down)
        if not self.ids.rv.data:
            self.ids.rv.data = [
                {"text": artist} for artist in self.ctrl.library.get_artists()]

    def on_leave(self):
        """ The screen is being exited. Removed the callback """
        self.ctrl.kb_handler.remove_callback(self.ids.rv.on_key_down)
        self.ids.rv.search_text = ""

    def item_selected(self, label, selected):
        """
        An label with the given text has been selected from the recycleview.
        """
        if selected:
            self.ctrl.show_screen("Albums", artist=label.text)
