"""
This module houses the main Zen PLayer widget, which itself contains the
screen manager and it's children,
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from ui.kvloader import KVLoader
from ui.screens.screens import ScreenFactory
# from kivy.uix.screenmanager import ScreenManager, FadeTransition
# sm = ObjectProperty(ScreenManager(transition=FadeTransition(duration=0.2)))
# """ A reference to the active ScreenManager class. """


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

    def show_screen(self, name="Playing", **kwargs):
        """
        Switch to the screen specified. The *kwargs* dictionary will be either
        passed to the constructor, or their values manually applied.
        """
        sm = self.ids.sm
        if name not in sm.screen_names:
            screen = ScreenFactory.get(name, ctrl=self.ctrl, **kwargs)
            sm.add_widget(screen)
        elif kwargs:
            screen = sm.get_screen(name)
            for key in kwargs.keys():
                setattr(screen, key, kwargs[key])
        sm.current = name
