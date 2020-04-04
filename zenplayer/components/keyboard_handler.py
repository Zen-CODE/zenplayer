"""
This module handles the keyboard integration for ZenPlayer
"""
from kivy.event import EventDispatcher
from kivy.core.window import Window
from kivy.utils import platform
from json import load
from os.path import join, dirname


class KeyHandler:
    """
    This class handles the keypress monitoring and event delegation.
    """
    def __init__(self, ctrl):
        super(KeyHandler, self).__init__()
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

    @staticmethod
    def _load_keymap():
        """ Load the specified key mappings from the json file. """
        with open(join(dirname(__file__), "keymap.json")) as f:
            mappings = load(f)
        return mappings["keymap"]

    def on_key_down(self, _keyboard, keycode, text, modifiers):
        """ React to the keypress event """
        print(f"KeyHandler: on_key_down - {keycode}")
        if modifiers:
            print("KeyHandler: no modifiers. Returning")
            return
        key_name = keycode[1]

        func = self.keymap.get(key_name, None)
        if func is not None:
            getattr(self.ctrl, func["name"])(**func.get("kwargs", {}))
            return True
        print(f"KeyHandler: No mapping found")
