"""
This module houses the Artist display UI
"""
from ui.screens.zenscreen import ZenScreen
from kivy.properties import StringProperty, BooleanProperty
from kivy.animation import Animation


class ArtistsScreen(ZenScreen):
    """
    Displays a interface for viewing and interacting with the artists
    list from the library.
    """

    note_text = StringProperty("Loading library. Please wait..")
    """
    The text, obtained from the keyboard, for searched for items in the list
    of atists.
    """

    show_note = BooleanProperty(True)
    """
    Boolean property dictating whether or not the notification label should
    be dispalyed.
    """

    search_text = StringProperty("")
    """
    Text entered by the user to move to the first artist staring with the
    text.
    """
    def on_enter(self):
        """
        As the loading can sometimes take time, do this once the screen is
        shown.
        """
        self.ctrl.kb_handler.add_callback(self.on_key_down)
        if not self.ids.rv.data:
            self.ids.rv.data = [
                {"text": artist} for artist in self.ctrl.library.get_artists()]
            self.note_text = ""

    def on_leave(self):
        """ The screen is being exited. Removed the callback """
        self.ctrl.kb_handler.remove_callback(self.on_key_down)

    def item_selected(self, label, selected):
        """
        An label with the given text has been selected from the recycleview.
        """
        if selected:
            self.ctrl.show_screen("Albums", artist=label.text)

    def on_show_note(self, widget, value):
        """ Either hide of show the note label """
        end_vale = 1 if value else 0
        Animation(opacity=end_vale, duration=2).start(self.ids.note_label)

    def on_note_text(self, widget, text):
        """ Handle the change of note text """
        self.show_note = bool(text)

    def on_key_down(self, keycode, text, modifiers):
        print(f"Got keydown {text}")