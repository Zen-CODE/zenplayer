"""
This module houses the screen displaying track information
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder


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
