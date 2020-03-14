"""
This module handles the keyboard integration for ZenPlayer
"""
from kivy.event import EventDispatcher
from kivy.core.window import Window
from kivy.utils import platform


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

    def on_key_down(self, _keyboard, keycode, text, _modifiers):
        """ React to the keypress event """
        key_name = keycode[1]
        print(f"Got keypress {key_name}")

        if key_name == "w":
            self.ctrl.volume_up()
        elif key_name == "s":
            self.ctrl.volume_down()
        elif key_name == "d":
            self.ctrl.move_forward()
        elif key_name == "a":
            self.ctrl.move_backward()
        elif key_name == "x":
            self.ctrl.play_pause()
        elif key_name == "z":
            self.ctrl.play_previous()
        elif key_name == "v":
            self.ctrl.stop()
        elif key_name == "b":
            self.ctrl.play_next()
        elif key_name == "f":
            self.ctrl.show_filebrowser()
        elif key_name == "p":
            self.ctrl.show_playlist()
        elif key_name == "s":
            self.ctrl.show_main()
        elif key_name == "q":
            self.ctrl.quit()

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
