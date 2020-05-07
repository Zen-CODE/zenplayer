"""
This module houses the main Zen PLayer widget, which itself contains the
screen manager and it's children,
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from ui.kvloader import KVLoader
from ui.screens.screens import ScreenFactory


class ZenPlayer(FloatLayout):
    """
    This class presents the persistanct elements of the ZenPlayer interface.
    """
    header = StringProperty("ZenPlayer")
    """ The header dispalyed on the top of the screen. This is changed when
    switching ZenScreen's.
    """

    ctrl = ObjectProperty()
    """ Reference to the Controller singleton """

    def __init__(self, **kwargs):
        KVLoader.load("ui/widgets/zenplayer.kv")
        super().__init__(**kwargs)
        self.show_screen()

    def show_screen(self, name="Playing", **kwargs):
        """
        Switch to the screen specified. The *kwargs* dictionary will be either
        passed to the constructor, or their values manually applied.
        """
        sm = self.ids.sm
        if name not in sm.screen_names:
            screen = ScreenFactory.get(name, ctrl=self.ctrl, **kwargs)
            sm.add_widget(screen)
        else:
            screen = sm.get_screen(name)
            if kwargs:
                for key in kwargs.keys():
                    setattr(screen, key, kwargs[key])
        sm.current = name
        self.set_header(screen.header)

    def set_header(self, header):
        """ Set the header for the screen """
        self.header = header
