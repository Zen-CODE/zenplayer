from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from audioplayer import Sound
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
# from kivy3dgui.layout3d import Layout3D


class MediaButton(FloatLayout):
    """
    A pretty, shiny button showing the player controls
    """
    source = StringProperty('')

    def __init__(self, **kwargs):
        """ Override the constructor so we can register an event """
        super(MediaButton, self).__init__(**kwargs)
        self.register_event_type("on_click")

    def on_click(self):
        """ The button has been clicked. """
        pass


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    but_playpause = ObjectProperty()
    ctrl = ObjectProperty(None)

    def __init__(self, ctrl, **kwargs):
        self.ctrl = ctrl
        Builder.load_file("ui/playing.kv")
        super(PlayingScreen, self).__init__(**kwargs)

        # if self.ctrl.kivy3dgui:
        #   from kivy.animation import Animation
        #   t = 'in_out_sine'
        #   anims = Animation(rotate=(360.0, 1, 0, 0), duration=7, t=t) + \
        #        Animation(rotate=(-360.0, 1, 0, 0), duration=7, t=t)
        #   anims = Animation(rotate=(360.0, 1, 0, 0), duration=5, t=t) + \
        #         Animation(rotate=(0.0, 1, 0, 0), duration=5, t=t) + \
        #       Animation(rotate=(360.0, 0, 1, 0), duration=5, t=t) + \
        #       Animation(rotate=(0.0, 0, 1, 0), duration=5, t=t)
        #   anims.repeat = True
        #    anims.start(self.ids.node)

    def on_sound_state(self, state):
        """ React to the change of state of the sound """
        if state == "playing":
            self.but_playpause.source = "images/pause.png"
        else:
            self.but_playpause.source = "images/play.png"

