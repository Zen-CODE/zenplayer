"""
This module adds global hotkey support from ZenPlayer
"""
from keyboard import add_hotkey
from os.path import join, exists
from json import load
from kivy.clock import Clock
from kivy.utils import platform
from components.paths import rel_to_base
from kivy.logger import Logger


class HotKeyHandler:
    """
    This class add global hotkey for calling ZenPlayer funtions. Hotkey
    bindings are set via the `hotkey.json` file in this folder.
    """
    _hk_map = None
    """ A dictionary containing the currently loaded hotkey map """

    @staticmethod
    def add_bindings(ctrl):
        """ Add the specified keybinding to action on the given controller. """
        Logger.info("HotKeyHandler: Adding bindings...")
        mapping = HotKeyHandler._load_hotkeymap()
        HotKeyHandler._create_bindings(mapping, ctrl)

    @staticmethod
    def _load_hotkeymap():
        """
        Return the specified hotkey mappings. Load from the json file if
        we have not done that already.
        """
        if HotKeyHandler._hk_map is not None:
            return HotKeyHandler._hk_map

        file_path = rel_to_base("config")
        if exists(join(file_path, f"hotkeymap_{platform}.json")):
            file_path = join(file_path, f"hotkeymap_{platform}.json")
        else:
            file_path = join(file_path, f"hotkeymap.json")

        with open(file_path) as f:
            mappings = load(f)
        return mappings["hotkeymap"]

    @staticmethod
    def get_function(ctrl, method):
        """ Return a function that calls the *method* of the *ctrl* but on the
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
        try:
            for key, method in mapping.items():
                add_hotkey(key, HotKeyHandler.get_function(ctrl, method))
        except ImportError:
            Logger.warning("HotKeyHandler: Load failed. Please run as root to "
                           "enable hotkey support")
