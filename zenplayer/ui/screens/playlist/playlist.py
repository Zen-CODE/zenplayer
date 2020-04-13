"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from ui.widgets.zenrecycleview import SelectableLabel
from kivy.clock import Clock
from ui.screens.zenscreen import ZenScreen


class PlaylistScreen(ZenScreen):
    """
    Displays the playlist along with some simple editing options.
    """
    current = NumericProperty(-1)
    """ The index of the currently playing track in the queue. """

    def on_selected(self, index, text):
        """ Handle the selection event """
        data = self.ctrl.playlist.get_info(index=index)
        PlaylistPopup(
            title="Track: {artist} - {album} - {track}".format(**data),
            ctrl=self.ctrl,
            index=index).open()


class PlaylistLabel(SelectableLabel):
    """ Add selection support to the Label """
    current_track = BooleanProperty(False)

    def _set_back_color(self):
        """ Set the back color of the label considering the playlist """
        if self.current_track:
            self.back_color = [.5, 1.0, .50, .3]
        else:
            super()._set_back_color()

    def on_current_track(self, _widget, _value):
        self._set_back_color()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.current_track = bool(rv.current == index)
        return super().refresh_view_attrs(rv, index, data)


class PlaylistPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    ctrl = ObjectProperty()
    """ A reference to the controller object"""

    index = NumericProperty()
    """ The index of the selected track in the Playlist.queue"""

    def button_play(self):
        """ Play the track selected track. """
        self.ctrl.play_index(self.index)

    def button_info(self):
        """ Display detailed info on the selected track """
        data = self.ctrl.playlist.queue[self.index]
        self.ctrl.show_screen("Info", filename=data["filename"])

    def button_remove(self):
        """ Play the track selected track. """
        self.ctrl.playlist.remove_index(self.index)
