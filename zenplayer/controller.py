from playlist import PlayList, PlayListScreen
from filebrowser import ZenFileBrowser
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from playing import PlayingScreen
from audioplayer import Sound
from kivy.properties import NumericProperty, ObjectProperty
from kivy.event import EventDispatcher

from kivy.clock import Clock
from os.path import join, expanduser, exists
from os import mkdir
from keyboard_handler import KeyHandler


class Controller(EventDispatcher):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """
    volume = NumericProperty(1.0)

    app = ObjectProperty()

    advance = True
    ''' Indicates whether to advance to the next track once the currently
    playing one had ended or not .'''

    sm = None
    ''' A Reference to the active ScreenManager class. '''

    pos = 0
    ''' Stores the current position in the currently playing audio file. '''

    kivy3dgui = False
    ''' Set whether to use the kivy3dgui interface on not '''

    def __init__(self, **kwargs):
        """ Initialize the screens and the screen manager """
        self._store = JsonStore(join(self._get_settings_folder(),
                                     "zenplayer.json"))
        self.playlist = PlayList(self._store)

        self.sm = ScreenManager()
        self.playing = PlayingScreen(self, name="main")
        self.sm.add_widget(self.playing)
        self.sm.current = "main"

        self.kb_handler = KeyHandler(self)
        Sound.add_state_callback(self.playing.on_sound_state)
        Sound.add_state_callback(self._on_sound_state)

        super(Controller, self).__init__(**kwargs)
        if self._store.exists('state'):
            state = self._store.get("state")
            if "volume" in state.keys():
                self.volume = state["volume"]

    @staticmethod
    def _get_settings_folder():
        """ Return the folder when the setting file is stored. """
        path = expanduser("~/.zencode")
        if not exists(path):
            mkdir(path)
        return path

    def _on_sound_state(self, state):
        """ The sound state has changed. If the track played to the end,
        move to the next track."""
        if state == "finished" and self.advance:
            self.play_next()

    def get_current_art(self):
        return self.playlist.get_current_art()

    def get_current_info(self):
        return self.playlist.get_current_info()

    def get_current_file(self):
        return self.playlist.get_current_file()

    @staticmethod
    def get_pos_length():
        return Sound.get_pos_length()

    def volume_up(self):
        """ Turn the volume up """
        self.volume += 0.025

    def volume_down(self):
        """ Turn the volume down """
        self.volume -= 0.025

    def on_volume(self, _widget, value):
        """ Set the volume of the currently playing sound """
        if 0.0 > value:
            self.volume = 0.0
        elif value > 1.0:
            self.volume = 1.0
        else:
            Sound.set_volume(value)
            self.playing.volume_slider.value = value

    def move_forward(self):
        """ Move the current playing time 5s forward """
        pos, length = Sound.get_pos_length()
        if length and pos < length - 5:
            self.set_position((pos + 5.0) / length)

    def move_backward(self):
        """ Move the current playing time 5s backward """
        pos, length = Sound.get_pos_length()
        if length:
            if pos < 5.0:
                pos = 5.0
            self.set_position((pos - 5.0) / length)

    def play_index(self, index):
        """
        Play the track with the specified playlist index
        """
        Sound.stop()
        self.playlist.current = index
        self.play_pause()

    def play_pause(self):
        """ Play or pause the currently playing track """
        self.advance = True
        if Sound.state == "playing":
            self.pos, _x = Sound.get_pos_length()
            Sound.stop()
        else:
            audio_file = self.get_current_file()
            if audio_file:
                Sound.play(audio_file, self.volume)
                if self.pos > 0:
                    def set_pos(_dt):
                        Sound.seek(self.pos)
                        self.pos = 0
                    Clock.schedule_once(set_pos, 0.1)

    def play_next(self):
        """ Play the next track in the playlist. """

        Sound.stop()
        self.playlist.move_next()
        self.play_pause()

    def play_previous(self):
        """ Play the previous track in the playlist. """
        Sound.stop()
        self.playlist.move_previous()
        self.play_pause()

    @staticmethod
    def set_position(value):
        """ Set the playing position to the specified value. """
        Sound.set_position(value)

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume)
        if "filebrowser" in self.sm.screen_names:
            self.sm.get_screen("filebrowser").save(self._store)

    def show_filebrowser(self):
        """ Switch to the file browser screen """
        if not self.kivy3dgui:
            if "filebrowser" not in self.sm.screen_names:
                self.sm.add_widget(ZenFileBrowser(self,
                                                  self.playlist,
                                                  self._store,
                                                  name="filebrowser"))
            self.sm.current = "filebrowser"

        else:
            if "filebrowser" not in self.playing.ids.p_sm.screen_names:
                self.playing.ids.p_sm.add_widget(ZenFileBrowser(self,
                                                 self.playlist,
                                                 self._store,
                                                 name="filebrowser"))

            from kivy.animation import Animation
            player3d = self.playing.ids.player3d
            Animation.cancel_all(player3d)

            (Animation(
                look_at=[-33, 0, 20, -43, 0, -93, 0, 1, 0], duration=0.8) +
             Animation(
                 look_at=[-83, 0, -83, 33, 0, -83, 0, 1, 0], duration=0.8)
             ).start(player3d)

    def show_playlist(self):
        """ Switch to the playlist screen """
        if not self.kivy3dgui:
            if "playlist" not in self.sm.screen_names:
                self.sm.add_widget(PlayListScreen(self.sm,
                                                  self,
                                                  self.playlist,
                                                  name="playlist"))
            self.sm.current = "playlist"
        else:
            if "playlist" not in self.playing.ids.c_sm.screen_names:
                self.playing.ids.c_sm.add_widget(PlayListScreen(self.sm,
                                                 self,
                                                 self.playlist,
                                                 name="playlist"))
            player3d = self.playing.ids.player3d
            from kivy.animation import Animation

            Animation.cancel_all(player3d)

            (Animation(
                look_at=[33, 0, 20, 43, 0, -93, 0, 1, 0], duration=0.8) +
             Animation(
                 look_at=[83, 0, -83, -33, 0, -83, 0, 1, 0], duration=0.8)
             ).start(player3d)

    def show_main(self):
        """ Switch to the main playing screen"""
        if not self.kivy3dgui:
            self.sm.current = "main"
        else:
            from kivy.animation import Animation
            player3d = self.playing.ids.player3d
            Animation.cancel_all(player3d)

            (Animation(look_at=[33, 0, 20, 43, 0, -93, 0, 1, 0], duration=0.8)
             + Animation(look_at=[0, 0, 10, 0, 0, 0, 0, 1, 0], duration=0.8)
             ).start(player3d)

    def show_main_from_filebrowser(self):
        """ Switch to the main playing screen"""
        if not self.kivy3dgui:
            self.sm.current = "main"
        else:
            from kivy.animation import Animation
            player3d = self.playing.ids.player3d
            Animation.cancel_all(player3d)

            (Animation(
                look_at=[-33, 0, 20, -43, 0, -93, 0, 1, 0], duration=0.8) +
             Animation(
                 look_at=[0, 0, 10, 0, 0, 0, 0, 1, 0], duration=0.8)
             ).start(player3d)

    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        Sound.stop()

    def quit(self):
        """ Close the appllication """
        self.stop()
        self.app.stop()
