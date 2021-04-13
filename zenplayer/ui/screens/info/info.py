"""
This module houses the screen displaying track information
"""
from kivy.properties import StringProperty
from kivy.clock import Clock
from components.meta import Metadata
from kivy.logger import Logger
from ui.screens.zenscreen import ZenScreen


class InfoScreen(ZenScreen):
    """
    The main screen that shows whats currently playing
    """
    filename = StringProperty(None, allownone=True)
    """ Display the track with the given filename. If set to anything Falsy,
    the current track will be displayed and updated on track changing. We set
    to None so an empty string still trigger on `on_filename` event.
    """

    units = {"length": "s",
             "bitrate": " kbps",
             "sample_rate": " hz"}
    """
    Defines the list of unit suffixes to be used when displaying track
    metadata.
    """

    def _show_current_track(self, *_args):
        """ Display the currently playing track in the playlist """
        file_name = self.ctrl.playlist.get_current_file()
        if file_name:
            self._show(file_name)

    def on_filename(self, _widget, filename):
        """ Respond to the changing of the filename """
        if filename:
            Logger.info("InfoScreen: Unbinding. Set to fixed track.")
            self.ctrl.playlist.unbind(current=self._show_current_track)
            self.ctrl.playlist.unbind(queue=self._show_current_track)
            Clock.schedule_once(lambda dt: self._show(filename))
        else:
            Logger.info("InfoScreen: Binding to the current track.")
            Clock.schedule_once(self._show_current_track)
            self.ctrl.playlist.bind(current=self._show_current_track)
            self.ctrl.playlist.bind(queue=self._show_current_track)

    def _show(self, filename):
        """ Show all the details on the given filename """
        self._show_info(filename)
        self._show_meta(filename)
        self._show_art()

    def _show_info(self, filename):
        """ Populate the track info """
        data = self.ctrl.playlist.get_info(filename=filename)
        for key in ["artist", "album", "track_name", "track_number"]:
            self.ids[key].text = data[key]

    def _show_meta(self, filename):
        """ Populate the track info """
        meta = Metadata.get(filename)
        for key, value in meta.items():
            val = self.format_meta_value(key, value)
            self.ids[key].text = f"{key.title().replace('_', ' ')}: {val}"

    @staticmethod
    def format_meta_value(key, value):
        """ Return the prettily formatted string for the given key """
        if key == "length":
            value = f"{int(value / 60.0)}m {int(value % 60)}"
        unit = InfoScreen.units.get(key, "")
        return f"{value}{unit}"

    def _show_art(self):
        """ Populate the track info """
        ids = self.ids
        self.ids["image"].source = self.ctrl.library.get_cover_path(
            ids.artist.text, ids.album.text)
