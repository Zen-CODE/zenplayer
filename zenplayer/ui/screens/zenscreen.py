"""
Thos module houses the ZenScreen base class which serves a base for all
screens in this app.
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder


class ZenScreen(Screen):
    """
    Serves as a Base class for screen in the the ZenPlayer app. It server to
    provide a `ctrl` binding and kv loading by default.
    """
    ctrl = ObjectProperty()
    """ A reference to the `Controller` object. """

    _loaded = []

    def __init__(self, **kwargs):
        ZenScreen.load_kv("ui/common.kv")
        ZenScreen.load_kv(
            "ui/screens/{0}/{0}.kv".format(kwargs["name"].lower()))
        super().__init__(**kwargs)

    @staticmethod
    def load_kv(file_name):
        """ Load commond kv, ensuring not to do it multiple times. """
        if file_name not in ZenScreen._loaded:
            Builder.load_file(file_name)
            ZenScreen._loaded.append(file_name)