"""
This module houses a mixin class to add keyboard seach suppport to the
ZenRecycleView class when loaded in a ZenScreen subclass
"""


class ZenKeyDown:
    """
    Mixin class to add keypress support to a ZenScreen when housing a
    ZenRecycleView
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
