"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from ui.common import Common


class PlaylistScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    ctrl = ObjectProperty()
    """ Reference to the controller """

    current = NumericProperty(-1)
    """ The index of the currently playing track in the queue. """

    def __init__(self, **kwargs):
        Common.load_common()
        Builder.load_file("ui/screens/playlist/playlist.kv")
        super().__init__(**kwargs)
