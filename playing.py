from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from audioplayer import Sound
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy3dgui.layout3d import Layout3D


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

    def on_source(self, widget, value):
        """ The 'source' property for the image has changed. Change it. """
        self.image.source = value

    def on_click(self):
        """ The button has been clicked. """
        pass


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    album_image = ObjectProperty()
    but_playpause = ObjectProperty()
    info_label = ObjectProperty()
    volume_slider = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = None  # The Controller

    def __init__(self, ctrl, **kwargs):
        Builder.load_file("playing.kv")
        self.ctrl = ctrl
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)
        self.volume_slider.value = self.ctrl.volume
        self.init_display()
        self.ids.player3d.look_at = [0, 0, 1, 0, 0, 0, 0, 1, 0]

    def init_display(self):
        """ Initialize the display """
        self.album_image.source = self.ctrl.get_current_art()
        info = self.ctrl.get_current_info()
        if info:
            self.info_label1.text = info["artist"]
            self.info_label2.text = info["album"]
            self.info_label3.text = info["file"]


        from kivy.animation import Animation
        t = 'in_out_sine'
        anims = Animation(rotate=(360.0, 1, 0, 0), duration=7, t=t) + \
            Animation(rotate=(-360.0, 1, 0, 0), duration=7, t=t)

        def repeat_anim(*args):
            Animation.cancel_all(self.ids.wings)
            self.ids.wings.rotate = (0, 0.0, 0.0, 1.0)
            anim = Animation (rotate=(359, 0.0, 0.0, 1.0), duration=2.0)
            anim.bind(on_complete=repeat_anim)
            anim.start(self.ids.wings)
        repeat_anim()

        def plane_anim(*args):
            Animation.cancel_all(self.ids.plane1)
            self.ids.plane1.rotate = (0, 0.0, 1.0, 0.0)
            anim = (Animation (rotate=(45, 0.1, 1.0, 0.0),
                              translate=(1.5, 2, -64),
                              duration=2.0, t=t) +
                   Animation(rotate=(180, 0.4, 1.0, 0.0),
                              translate=(19.5, -2, -74),
                              duration=2.0, t=t) +
                   Animation(rotate=(270, 0.2, 1.0, 0.0),
                              translate=(1.5, 2, -89),
                              duration=1.8, t=t) +
                   Animation(rotate=(360, 0.0, 1.0, 0.0),
                              translate=(-29.5, -2, -84),
                              duration=2.0, t=t))
            anim.bind(on_complete=plane_anim)
            anim.start(self.ids.plane1)
        plane_anim()

        def buildozer_anim(*args):
            Animation.cancel_all(self.ids.buildozer1)
            #self.ids.buildozer1.rotate = (90+45, 0.0, 1.0, 0.0)
            anim = (Animation (rotate=(90+45, 0.02, 1.0, 0.0),
                              duration=0.5, t=t) +
                    Animation (translate=(1.5, -18, -64),
                              duration=2.0, t=t) +
                    Animation(rotate=(180+45, 0.01, 1.0, 0.0),
                              duration=0.5, t=t) +
                    Animation(translate=(19.5, -18, -74),
                              duration=2.0, t=t) +
                    Animation(rotate=(270+45, 0.02, 1.0, 0.0),
                              duration=0.5, t=t) +
                    Animation(translate=(1.5, -18, -99),
                              duration=1.8, t=t) +
                    Animation(rotate=(360+45, 0.01, 1.0, 0.0),
                              duration=0.5, t=t) +
                    Animation(translate=(-29.5, -18, -84),
                              duration=2.0, t=t))
            anim.bind(on_complete=buildozer_anim)
            anim.start(self.ids.buildozer1)
        buildozer_anim()

        #anims.start(self.ids.node)

    def on_sound_state(self, state):
        """ React to the change of state of the sound """
        if state == "playing":
            self.but_playpause.source = "images/pause.png"
            self.init_display()
        else:
            self.but_playpause.source = "images/play.png"

    def _update_progress(self, dt):
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
