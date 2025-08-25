"""
This class houses the Playlist class for ZenPlayer
"""

from kivy.properties import NumericProperty
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
        Reload the data from the playlist queue. This is required to refr∂ßesh
        after items have been removed or added.
        """
        super().on_enter()
        self._reload_data()
        self.ctrl.playlist.bind(queue=self._reload_data)
        track = self.ctrl.playlist.get_current_info()
        self.ids.rv.find_item(track["track_name"])

    def on_leave(self):
        """Unregister our callback to monitor queue changes"""
        super().on_leave()
        self.ctrl.playlist.unbind(queue=self._reload_data)

    def _reload_data(self, *_args):
        """Reload the data from the playlist queue"""
        self.ids.rv.data = []
        self.ids.rv.data = self.ctrl.playlist.queue

    def item_touched(self, item):
        """Show the popup for selecting the index in the playlist"""
        data = self.ctrl.playlist.get_info(index=item.index)
        self.ctrl.zenplayer.show_screen(
            "Context",
            title="Track: {artist} - {album}: {track_number} - {track_name}".format(
                **data
            ),
            parent_screen="Playlist",
            actions=[
                {"text": "Play", "action": lambda: self.button_play(item.index)},
                {
                    "text": "Info",
                    "show_parent": False,
                    "action": lambda: self.button_info(item.index),
                },
                {"text": "Remove", "action": lambda: self.button_remove(item.index)},
                {"text": "Remove all", "action": self.button_clear_files},
                {"text": "Cancel", "action": lambda: None},
            ],
        )

    def button_play(self, index):
        """Play the track selected track."""
        self.ctrl.play_index(index)

    def button_info(self, index):
        """Display detailed info on the selected track"""
        data = self.ctrl.playlist.queue[index]
        self.ctrl.zenplayer.show_screen("Info", filename=data["filename"])

    def button_remove(self, index):
        """Play the track selected track."""
        self.ctrl.playlist.remove_index(index)

    def button_clear_files(self):
        """Remove all files from the playlist"""
        self.ctrl.playlist.clear_files()
