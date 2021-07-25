"""
This module handles the keyboard integration for ZenPlayer
"""
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
from components.config import Config
from functools import lru_cache


class KeyHandler:
    """
    This class handles the keypress monitoring and event delegation.
    """
    def __init__(self, ctrl):
        super().__init__()
        if platform in ['ios', 'android']:
            return

        self.kb_listener = Window.request_keyboard(
            lambda: None, None, 'text')
        self.kb_listener.bind(on_key_down=self.on_key_down)

        self.ctrl = ctrl
        self.keymap = self._load_keymap()
        """
        A dictionary of ("letter", "function_name") values specifying which
        keypresses (keys) should call which functions (values).
        """

        self._callbacks = []
        """ A list of functions which have requested to receives keyboard events
        """

    def add_callback(self, callback):
        """ Add a callback function to be called on keyboard event """
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        """ Add a callback function to be called on keyboard event """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    @staticmethod
    @lru_cache()
    def _load_keymap():
        """ Load the specified key mappings from the json file. """
        mappings = Config.load("keymap.json")
        return mappings["keymap"]

    @staticmethod
    def _is_normal_key(key):
        """
        Return True if the given character represents a normal key and not a
        modifier.
        """
        return len(key) == 1 or key in ["up", "down", "left", "right"]

    @staticmethod
    def _get_match(keymap, modifiers, key_name):
        """
        Return the value in the keymap that matches the modifiers and key_name
        """
        Logger.debug("keyboard_handler.py: _get_match: Look for "
                     "modifiers=%s, key_name=%s", modifiers, key_name)
        for key in keymap.keys():
            parts = key.split("+")
            hk_key_name = filter(KeyHandler._is_normal_key, parts)
            if next(hk_key_name, '') == key_name:
                # The letter matches. Do the modifiers?
                hk_modifiers = filter(
                    lambda x: not KeyHandler._is_normal_key(x), parts)
                if not set(hk_modifiers).difference(set(modifiers)):
                    return keymap[key]
        return None

    def on_key_down(self, _keyboard, keycode, text, modifiers):
        """ React to the keypress event """
        func = self._get_match(self._load_keymap(), modifiers, keycode[1])
        if text and not (text.isalpha() or text.isdigit()):
            return None
        if func is not None:
            # Lookup the function from the component if specified, else ctrl
            obj = self.ctrl if "component" not in func.keys() else \
                getattr(self.ctrl, func["component"])
            getattr(obj, func["name"])(**func.get("kwargs", {}))
            return True
        for cb in self._callbacks:
            cb(keycode, text, modifiers)
        return None
