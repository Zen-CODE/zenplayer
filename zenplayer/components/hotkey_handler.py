"""
This module adds global hotkey support from ZenPlayer
"""

from kivy.clock import Clock
from kivy.logger import Logger
from components.config import Config
from pynput.keyboard import GlobalHotKeys


class HotKeyHandler:
    """
    This class add global hotkey for calling ZenPlayer funtions. Hotkey
    bindings are set via the `hotkey.json` file in this folder.
    """

    @staticmethod
    def add_bindings(ctrl):
        """Add the specified keybinding to action on the given controller."""
        Logger.info("HotKeyHandler: Adding bindings...")
        mapping = HotKeyHandler._load_hotkeymap()
        HotKeyHandler._create_bindings(mapping, ctrl)

    @staticmethod
    def _load_hotkeymap():
        """
        Return the specified hotkey mappings. Load from the json file if
        we have not done that already.
        """
        mappings = Config.load("hotkeymap.json")
        return mappings["hotkeymap"]

    @staticmethod
    def get_function(ctrl, method):
        """Return a function that calls the *method* of the *ctrl* but on the
        next clock event. This (hopefully) prevents segmentation faults.
        """
        func = getattr(ctrl, method)
        return lambda: Clock.schedule_once(lambda dt: func())

    @staticmethod
    def _create_bindings(mapping, ctrl):
        """
        Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        mapdict = {k: HotKeyHandler.get_function(ctrl, v) for k, v in mapping.items()}
        ghk = GlobalHotKeys(mapdict)
        ghk.start()
