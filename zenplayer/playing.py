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
    image = ObjectProperty()

    def __init__(self, **kwargs):
        """ Override the constructor so we can register an event """
        super(MediaButton, self).__init__(**kwargs)
        self.register_event_type("on_click")

    def on_source(self, _widget, value):
        """ The 'source' property for the image has changed. Change it. """
        self.image.source = value

    def on_click(self):
        """ The button has been clicked. """
        pass


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    but_playpause = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = ObjectProperty(None)

    def __init__(self, ctrl, **kwargs):
        self.ctrl = ctrl
        Builder.load_file("playing.kv")
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)

    def on_sound_state(self, state):
        """ React to the change of state of the sound """
        if state == "playing":
            self.but_playpause.source = "images/pause.png"
        else:
            self.but_playpause.source = "images/play.png"

    def _update_progress(self, _dt):
        """ Update the progressbar  """
        if Sound.state == "playing":
            pos, length = Sound.get_pos_length()
            if length > 0:
                self.progress_slider.value = pos / length

                self.time_label.text = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
