"""
This module houses the screen displaying track information
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from components.meta import Metadata
from kivy.logger import Logger


class InfoScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    ctrl = ObjectProperty(None)

    filename = StringProperty(allownone=True)
    """ Display the track with the given filename. If set to None, the current
    track will be displayed and updated on track changing.
    """

    units = {"length": " s",
             "bitrate": " kbps",
             "sample_rate": " hz"}
    """
    Defines the list of unit suffixes to be used when displaying track metadata.
    """

    def __init__(self, **kwargs):
        Builder.load_file("ui/screens/info/info.kv")
        super().__init__(**kwargs)

    def _show_current_track(self, *args):
        """ Display the currently playing track in the playlist """
        self._show(self.ctrl.playlist.get_current_file())

    def on_filename(self, _widget, filename):
        """ Respond to the changing of the filename """
        if filename is None:
            Logger.info("InfoScreen: Binding to the current track.")
            Clock.schedule_once(self._show_current_track)
            self.ctrl.playlist.bind(current=self._show_current_track)
            self.ctrl.playlist.bind(queue=self._show_current_track)
        else:
            Logger.info("InfoScreen: Unbinding. Set to fixed track.")
            self.ctrl.playlist.unbind(current=self._show_current_track)
            self.ctrl.playlist.unbind(queue=self._show_current_track)
            Clock.schedule_once(lambda dt: self._show(filename))

    def _show(self, filename):
        """ Show all the details on the given filename """
        self._show_info(filename)
        self._show_meta(filename)
        self._show_art(filename)

    def _show_info(self, filename):
        """ Populate the track info """
        data = self.ctrl.playlist.get_info(filename=filename)
        for key in data.keys():
            self.ids[key].text = data[key]
        self.ids["filename"].text = filename

    def _show_meta(self, filename):
        """ Populate the track info """
        meta = Metadata.get(filename)
        for key in meta.keys():
            val = self.format_meta_value(key, meta[key])
            self.ids[key].text = f"{key.title().replace('_', ' ')}: {val}"

    @staticmethod
    def format_meta_value(key, value):
        """ Return the prettily formatted string for the given key """
        if not isinstance(value, str):
            val = int(value)  # Present horrible decimal values...
        unit = InfoScreen.units.get(key, "")
        return f"{value}{unit}"

    def _show_art(self, filename):
        """ Populate the track info """
        self.ids["image"].source = self.ctrl.playlist.get_album_art(filename)
