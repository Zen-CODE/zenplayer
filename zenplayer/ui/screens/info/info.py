"""
This module houses the screen displaying track information
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock


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
        Clock.schedule_once(lambda dt: self._show_info(filename))

    def _show_info(self, filename):
        """ Populate the track info """
        data = self.ctrl.playlist.get_info(filename=filename)
        for key in data.keys():
            self.ids[key].text = data[key]
        self.ids["filename"] = filename

    def _show_details(self, filename):
        """ Populate the track info """
        pass
