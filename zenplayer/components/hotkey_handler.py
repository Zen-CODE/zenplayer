"""
This module adds global hotkey support from ZenPlayer
"""
from keyboard import add_hotkey
from os.path import join, dirname
from json import load


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
    def _create_bindings(mapping, ctrl):
        """
        Create hotkey bindings from the mapping to the controller actions.

        Args:
            mapping a dictionary with the key as the hotkey combination and the
            value as the controller action.
        """
        for key, value in mapping.items():
            add_hotkey(key, getattr(ctrl, value))
