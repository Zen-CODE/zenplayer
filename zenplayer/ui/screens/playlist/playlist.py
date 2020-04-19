"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from ui.screens.zenscreen import ZenScreen
from ui.widgets.zenkeydown import ZenKeyDown


class PlaylistScreen(ZenKeyDown, ZenScreen):
    """
    Displays the playlist along with some simple editing options.
    """
    current = NumericProperty(-1)
    """ The index of the currently playing track in the queue. """

    def on_enter(self):
        """
        Relod the data from the playlist queue. This is required to refesh
        after items have been removed or added.
        """
        super().on_enter()
        self.ids.rv.data = []
        self.ids.rv.data = self.ctrl.playlist.queue

    def item_touched(self, item):
        """ Show the popup for selecting the index in the playlist """
        data = self.ctrl.playlist.get_info(index=item.index)
        PlaylistPopup(
            title="Track: {artist} - {album} - {track}".format(**data),
            screen=self,
            index=item.index).open()

    def item_draw(self, label):
        """ Set the back color of the label considering the playlist """
        if label.index == self.current:
            label.back_color = [.5, 1.0, .50, .3]
            return True
        return False

    def button_play(self, index):
        """ Play the track selected track. """
        self.ctrl.play_index(index)

    def button_info(self, index):
        """ Display detailed info on the selected track """
        data = self.ctrl.playlist.queue[index]
        self.ctrl.show_screen("Info", filename=data["filename"])

    def button_remove(self, index):
        """ Play the track selected track. """
        self.ctrl.playlist.remove_index(index)
        self.on_pre_enter()

    def button_clear_files(self):
        """ Remove all files from the playlist """
        self.ctrl.playlist.clear_files()
        self.on_pre_enter()


class PlaylistPopup(Popup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    screen = ObjectProperty()
    """ A reference to the Playlist screen"""

    index = NumericProperty()
    """ The index of the selected track in the Playlist.queue"""
