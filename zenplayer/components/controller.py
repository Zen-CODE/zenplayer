from ui.screens.playlist.playlist import Playlist, PlaylistScreen
from ui.screens.filebrowser.filebrowser import ZenFileBrowser
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from ui.screens.playing.playing import PlayingScreen
from components.audioplayer import Sound
from kivy.properties import (NumericProperty, ObjectProperty, StringProperty,
                             OptionProperty)
from kivy.event import EventDispatcher
from kivy.clock import Clock
from os.path import join, expanduser, exists
from os import mkdir, sep
from components.keyboard_handler import KeyHandler
from components.hotkey_handler import HotKeyHandler
from components.filedrop import FileDrop


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
    state = OptionProperty("", options=["stopped", "paused", "playing", ""])
    prev_state = None

    position = NumericProperty(0.0)
    """ Position is the track as a fraction between 0 and 1. """

    # The following is used to trigger the above
    file_name = StringProperty("")

    app = ObjectProperty()

    playlist = ObjectProperty()
    """ Reference to the Playlist object. """

    sm = None
    ''' A Reference to the active ScreenManager class. '''

    kivy3dgui = False
    ''' Set whether to use the kivy3dgui interface on not '''

    prune = True
    """ If set to true, remove files from the playlist once played. """

    def __init__(self, **kwargs):
        """ Initialize the screens and the screen manager """
        super(Controller, self).__init__(**kwargs)
        self._store = JsonStore(join(self._get_settings_folder(),
                                     "zenplayer.json"))
        self.playlist = Playlist(self._store)
        self.file_drop = FileDrop(self.playlist)
        self.advance = True

        self.sm = ScreenManager()
        self.playing = PlayingScreen(self, name="main")
        self.sm.add_widget(self.playing)
        self.sm.current = "main"

        HotKeyHandler.add_bindings(self)
        self.kb_handler = KeyHandler(self)
        self.sound = Sound()
        self.sound.bind(state=self.set_state)
        Clock.schedule_interval(self._update_progress, 1/5)

        self._restore_state()

    def _restore_state(self):
        """ Load the state when previously exited if possible. """
        if "state" in self._store.keys():
            state = self._store.get("state")
            for key, value in state.items():
                setattr(self, key, value)

    def set_state(self, _widget, value):
        """
        Set the state of the currently playing track. This is the callback
        fired when the media player encounters the end of track.
        """
        if value == "stopped" and self.state != "stopped":
            if self.advance:
                self.play_next()

    def on_state(self, _widget, value):
        """ React to the change of state event """
        if value == "playing":
            if self.sound.state == "playing":
                self.sound.stop()
            self.file_name = self.playlist.get_current_file()
            if self.file_name:
                pos = 0 if self.prev_state != "paused" else self.position
                self.sound.play(self.file_name, self.volume, pos)
        elif value == "stopped":
            self.sound.stop()
        elif value == "paused" and self.prev_state is not None:
            # If the prev_state is None, we have just restored state on start
            self.position, _length = self.sound.get_pos_length()
            self.sound.pause()

        self.prev_state = value

    @staticmethod
    def _get_settings_folder():
        """ Return the folder when the setting file is stored. """
        path = expanduser("~/.zencode")
        if not exists(path):
            mkdir(path)
        return path

    def _update_progress(self, _dt):
        """ Update the progressbar  """
        if self.sound.state == "playing":
            pos, length = self.sound.get_pos_length()
            pos_secs = pos * length
            if length > 0:
                self.time_display = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos_secs / 60),
                    int(pos_secs % 60),
                    int(length / 60),
                    int(length % 60))
                self.position = pos

    def on_file_name(self, _widget, value):
        """ Respond to the change of file name and set the info fields."""
        parts = value.split(sep)
        if len(parts) > 2:
            self.track = parts[-1]
            self.album = parts[-2]
            self.artist = parts[-3]
            self.cover = self.playlist.get_album_art(value)

    def volume_up(self):
        """ Turn the volume up """
        self.volume += 0.025

    def volume_down(self):
        """ Turn the volume down """
        self.volume -= 0.025

    def on_volume(self, _widget, value):
        """ Set the volume of the currently playing sound """
        self.volume = abs(value) % 1.0 if value < 1 else 1
        self.sound.set_volume(value)

    def move_forward(self):
        """ Move the current playing time 5s forward """
        pos, length = self.sound.get_pos_length()
        if length:
            one_sec = 1 / length
            if pos + 5 * one_sec < 1:
                self.set_position(pos + 5 * one_sec)

    def move_backward(self):
        """ Move the current playing time 5s backward """
        pos, length = self.sound.get_pos_length()
        if length:
            one_sec = 1 / length
            if pos - 5 * one_sec > 0:
                self.set_position(pos - 5 * one_sec)

    def play_index(self, index):
        """
        Play the track with the specified playlist index
        """
        self.stop()
        self.playlist.current = index
        self.play_pause()

    def play_pause(self):
        """ Play or pause the currently playing track """
        if self.state == "playing":
            self.state = "paused"
        else:
            self.state = "playing"

    def play_next(self):
        """ Play the next track in the playlist. """
        self.advance = False
        self.stop()
        if self.prune:
            self.playlist.remove_current()
        else:
            self.playlist.move_next()
        self.position = 0
        self.play_pause()
        self.advance = True

    def play_previous(self):
        """ Play the previous track in the playlist. """
        self.advance = False
        self.stop()
        self.position = 0
        self.playlist.move_previous()
        self.play_pause()
        self.advance = True

    def set_position(self, value):
        """ Set the playing position to the specified value. """
        self.position = value
        self.sound.set_position(value)

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume, position=self.position,
                        state=self.state)
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
                self.sm.add_widget(PlaylistScreen(ctrl=self, name="playlist"))
            self.sm.current = "playlist"
        else:
            if "playlist" not in self.playing.ids.c_sm.screen_names:
                self.playing.ids.c_sm.add_widget(
                    PlaylistScreen(ctrl=self, name="playlist"))
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
        self.state = "stopped"
        self.advance = True

    def quit(self):
        """ Close the appllication """
        if self.state == "playing":
            self.state = "paused"  # Enable saving of position
        self.save()
        self.stop()
        Clock.schedule_once(lambda dt: self.app.stop())
