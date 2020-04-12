"""
Thos module houses the ZenScreen base class which serves a base for all
screens in this app.
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from ui.kvloader import KVLoader


class ZenScreen(Screen):
    """
    Serves as a Base class for screen in the the ZenPlayer app. It server to
    provide a `ctrl` binding and kv loading by default.
    """
    ctrl = ObjectProperty()
    """ A reference to the `Controller` object. """

    def __init__(self, **kwargs):
        KVLoader.load("ui/common.kv")
        KVLoader.load("ui/screens/{0}/{0}.kv".format(kwargs["name"].lower()))
        super().__init__(**kwargs)
