"""
This module houses the Zen Music Library browser based on the recycleview
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty


class ArtistsScreen(Screen):
    """
    Displays a interface for viewing and interacting with the `Library`
    component
    """
    ctrl = ObjectProperty(None)

    def __init__(self, ctrl, **kwargs):
        self.ctrl = ctrl
        Builder.load_file("ui/screens/library/artists.kv")
        super().__init__(**kwargs)
