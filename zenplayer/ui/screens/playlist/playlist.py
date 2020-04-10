"""
This class houses the Playlist class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.lang import Builder


class PlaylistScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    ctrl = ObjectProperty()
    """ Reference to the controller """

    current = NumericProperty(-1)
    """ The index of the currently playing track in the queue. """

    def __init__(self, **kwargs):
        Builder.load_file("ui/screens/playlist/playlist.kv")
        super(PlaylistScreen, self).__init__(**kwargs)
