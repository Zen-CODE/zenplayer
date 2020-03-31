"""
This module adds global hotkey support from ZenPlayer
"""
from keyboard import add_hotkey
from os.path import join, dirname
from json import load
from kivy.clock import Clock
from kivy.utils import platform


class HotKeyHandler:
    """
    This class add global hotkey for calling ZenPlayer funtions. Hotkey
    bindings are set via the `hotkey.json` file in this folder.
    """
    @staticmethod
    def add_bindings(ctrl):
        """ Add the specified keybinding to action on the given controller. """
        mapping = HotKeyHandler._load_hotkeymap()
        HotKeyHandler._create_bindings(mapping, ctrl)

    @staticmethod
    def _load_hotkeymap():
        """ Load the specified hotkey mappings from the json file. """
        with open(join(dirname(__file__), "hotkeymap.json")) as f:
            mappings = load(f)
        return mappings["hotkeymap"]

    @staticmethod
    def get_function(ctrl, method):
        """ Return a function that calls the *method* of the *ctrl* but on the
        next clock event. This (hopefully) prevents segmentation faults.
        """
        func = getattr(ctrl, method)
        return Clock.schedule_once(lambda dt: func())

    @staticmethod
    def _create_bindings(mapping, ctrl):
        """
        Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        try:
            for key, method in mapping.items():
                if platform == "macosx":
                    key = key.replace("alt", "command")
                add_hotkey(key, HotKeyHandler.get_function(ctrl, method))