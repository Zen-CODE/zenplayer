"""
This module houses a shared ZenPopup class, for presenting consistent UI popups
in the ZenPlayer application.
"""
from kivy.uix.popup import Popup
from kivy.logger import Logger
from ui.kvloader import KVLoader  # pylint: disable=import-error
from kivy.properties import ObjectProperty


class ZenPopup(Popup):
    """
    A standardised ZenPlayer popup.
    """
    handler = ObjectProperty()
    """ A reference to the object that should handle the Popup interactions """

    _instance = None
    """
    Reference to the underlying popup instance, This is controlled to ensure
    only one popup at a time is created.
    """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenpopup.kv")
        super().__init__(**kwargs)

    def open(self):
        """ Open an instance of the specified Popup. Do nothing if a popup
        already exists.
        """
        if ZenPopup._instance is None:
            ZenPopup._instance = self
            super().open()
        else:
            Logger.warning("ZenPopup: Attempting to show duplicate popup")

    def dismiss(self):
        """ Dismiss the current popup """
        Logger.info("ZenPopup: Dismising instance ")
        ZenPopup._instance = None
        super().dismiss()
