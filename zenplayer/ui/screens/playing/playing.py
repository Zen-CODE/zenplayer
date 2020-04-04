from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from components.audioplayer import Sound
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
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


class VolumeSlider(Slider):
    """
    A volume slider that allows smooth volume changes, rather that waiting for
    the end of the slide.
    """
    ctrl = ObjectProperty()

    dragging = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
        return super(VolumeSlider, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging:
            self.ctrl.on_volume(None, self.value)
        return super(VolumeSlider, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        self.dragging = False
        return super(VolumeSlider, self).on_touch_up(touch)


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    ctrl = ObjectProperty(None)

    def __init__(self, ctrl, **kwargs):
        self.ctrl = ctrl
        Builder.load_file("ui/screens/playing/playing.kv")
        Builder.load_file("ui/common.kv")
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
