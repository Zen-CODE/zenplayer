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

    def item_touched(self, index):
        """ Show the popup for selecting the specified index in the playlist """
        data = self.ctrl.playlist.get_info(index=index)
        PlaylistPopup(
            title="Track: {artist} - {album} - {track}".format(**data),
            ctrl=self.ctrl,
            index=index).open()

    def set_label_back_color(self, label):
        """ Set the back color of the label considering the playlist """
        if label.index == self.current:
            label.back_color = [.5, 1.0, .50, .3]
        else:
            super().set_back_color()


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
