"""
This module houses the screen displaying track information
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from components.meta import  Metadata


class InfoScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    ctrl = ObjectProperty(None)

    filename = StringProperty()

    def __init__(self, ctrl, **kwargs):
        self.ctrl = ctrl
        Builder.load_file("ui/screens/info/info.kv")
        super(InfoScreen, self).__init__(**kwargs)

    def on_filename(self, _widget, filename):
        """ Respond to the changing of the filename """
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
            self.ids[key].text = f"{key.title()}: {meta[key]}"

    def _show_art(self, filename):
        """ Populate the track info """
        self.ids["image"].source = self.ctrl.playlist.get_album_art(filename)
