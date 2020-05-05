"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.properties import NumericProperty
from ui.widgets.zenpopup import ZenPopup
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
        self._reload_data()
        self.ctrl.playlist.bind(queue=self._reload_data)

    def on_leave(self):
        """ Unregister our callback to monitor queue changes """
        self.ctrl.playlist.unbind(queue=self._reload_data)

    def _reload_data(self, *args):
        """ Reload the data from the playlist queue """
        self.ids.rv.data = []
        self.ids.rv.data = self.ctrl.playlist.queue

    def item_touched(self, item):
        """ Show the popup for selecting the index in the playlist """
        data = self.ctrl.playlist.get_info(index=item.index)
        PlaylistPopup(
            title="Track: {artist} - {album}: {track_number} - {track_name}"
                  .format(**data),
            handler=self,
            index=item.index).open()

    def button_play(self, index):
        """ Play the track selected track. """
        self.ctrl.play_index(index)

    def button_info(self, index):
        """ Display detailed info on the selected track """
        data = self.ctrl.playlist.queue[index]
        self.ctrl.zenplayer.show_screen("Info", filename=data["filename"])

    def button_remove(self, index):
        """ Play the track selected track. """
        self.ctrl.playlist.remove_index(index)
        self.on_pre_enter()

    def button_clear_files(self):
        """ Remove all files from the playlist """
        self.ctrl.playlist.clear_files()
        self.on_enter()


class PlaylistPopup(ZenPopup):
    """
    The Popup show when the playlist item is tapped and held.
    """
    index = NumericProperty()
    """ The index of the selected track in the Playlist.queue"""
