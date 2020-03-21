from playlist import PlayList, PlayListScreen
from filebrowser import ZenFileBrowser
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from playing import PlayingScreen
from audioplayer import Sound
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.clock import Clock
from os.path import join, expanduser, exists
from os import mkdir, sep
from keyboard_handler import KeyHandler


DEFAULT_COVER = "images/zencode.jpg"


class Controller(EventDispatcher):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """

    # The following fields control the display in the playlist
    volume = NumericProperty(1.0)
    artist = StringProperty("-")
    album = StringProperty("-")
    track = StringProperty("-")
    cover = StringProperty(DEFAULT_COVER)
    time_display = StringProperty("-")

    # The following is used to trigger the above
    file_name = StringProperty("")

    app = ObjectProperty()

    advance = True
    ''' Indicates whether to advance to the next track once the currently
    playing one had ended or not .'''

    sm = None
    ''' A Reference to the active ScreenManager class. '''

    pos = NumericProperty(1.0)
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
        self.timer_event = None

        super(Controller, self).__init__(**kwargs)
        if self._store.exists('state'):
            state = self._store.get("state")
            for key, value in state.items():
                setattr(self, key, value)

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
        print(f"Controller.On_sound_state fired. state={state}. "
              f"advance={self.advance}")
        if state == "stopped":
            if self.advance:
                Clock.schedule_once(lambda dt: self.play_next())
            if self.timer_event is not None:
                self.timer_event.cancel()
        else:
            self.timer_event = Clock.schedule_interval(
                self._update_progress, 1/25)

    def _update_progress(self, _dt):
        """ Update the progressbar  """
        if Sound.state == "playing":
            pos, length = Sound.get_pos_length()
            if length > 0:
                self.time_display = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
        else:
            self.time_display = "-"

    def on_file_name(self, widget, value):
        """ Respond to the change of file name and set the info fields."""
        parts = value.split(sep)
        if len(parts) > 2:
            self.track = parts[-1]
            self.album = parts[-2]
            self.artist = parts[-3]
            self.cover = self.playlist.get_albumart(value)

    def get_current_info(self):
        return self.playlist.get_current_info()

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
        self.volume = abs(value) % 1.0 if value < 1 else 1
        Sound.set_volume(value)

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
        if Sound.state == "playing":
            self.pos, _x = Sound.get_pos_length()
            self.stop()
        else:
            self.advance = True
            self.file_name = self.playlist.get_current_file()
            if self.file_name:
                Sound.play(self.file_name, self.volume)
                if self.pos > 0:
                    Sound.seek(self.pos)

    def play_next(self):
        """ Play the next track in the playlist. """
        self.stop()
        self.playlist.move_next()
        self.play_pause()

    def play_previous(self):
        """ Play the previous track in the playlist. """
        self.stop()
        self.playlist.move_previous()
        self.play_pause()

    def set_position(self, value):
        """ Set the playing position to the specified value. """
        self.pos = value
        Sound.set_position(value)

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume, pos=self.pos)
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
