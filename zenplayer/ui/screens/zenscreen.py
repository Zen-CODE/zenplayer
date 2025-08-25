"""
Thos module houses the ZenScreen base class which serves a base for all
screens in this app.
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from ui.kvloader import KVLoader


class ZenScreen(Screen):
    """
    Serves as a Base class for screen in the the ZenPlayer app. It server to
    provide a `ctrl` binding and kv loading by default.
    """

    ctrl = ObjectProperty()
    """ A reference to the `Controller` object. """

    header = StringProperty()
    """ Sets the text to be displayed as a header in the ZenPlayer header area.
    """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenbutton.kv")
        KVLoader.load("ui/screens/{0}/{0}.kv".format(kwargs["name"].lower()))
        super().__init__(**kwargs)
