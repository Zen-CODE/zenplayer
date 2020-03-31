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

        self.kb_listener = ZenKeyboardListener(self.on_key_down,
                                               ctrl.playing)
        self.ctrl = ctrl
        self.keymap = self._load_keymap()
        """
        A dictionary of ("letter", "function_name") values specifying which
        keypresses (keys) should call which functions (values).
        """

    def _load_keymap(self):
        """ Load the specified key mappings from the json file. """
        with open(join(dirname(__file__), "keymap.json")) as f:
            mappings = load(f)
        return mappings["keymap"]

    def on_key_down(self, _keyboard, keycode, text, modifiers):
        """ React to the keypress event """
        if modifiers:
            return
        key_name = keycode[1]

        func = self.keymap.get(key_name, None)
        if func is not None:
            getattr(self.ctrl, func)()
            return True


class ZenKeyboardListener(EventDispatcher):
    """
    This class handles the management of keypress to control volume, play,
    stop, next etc.
    """
    def __init__(self, callback, widget):
        super(ZenKeyboardListener, self).__init__()
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, widget, 'text')
        self._keyboard.bind(on_key_down=callback)
        self._cb = callback

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._cb)
        self._keyboard = None
        self._cb = None
