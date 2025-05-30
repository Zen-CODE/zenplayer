from kivy.properties import (  # pylint: disable=no-name-in-module
    NumericProperty, ObjectProperty, StringProperty, OptionProperty)
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.logger import Logger
from os import sep
from components.keyboard_handler import KeyHandler
from components.hotkey_handler import HotKeyHandler
from components.library import Library
from components.playlist import Playlist
from components.store import StoreFactory
from components.paths import rel_to_base
from kivy.core.window import Window
from ui.widgets.zenplayer import ZenPlayer
from components.audio import SoundLoader, register_vlc
from os import environ
from components.cloud_firestore import NowPlaying


class Controller(EventDispatcher):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays.
    """

    volume = NumericProperty(1.0)
    artist = StringProperty("-")
    album = StringProperty("-")
    track = StringProperty("-")
    cover = StringProperty(rel_to_base("images", "zencode.png"))
    time_display = StringProperty("-")
    state = OptionProperty("", options=["Stopped", "Paused", "Playing", ""])

    position = NumericProperty(0.0)
    """ Position is the track as a fraction between 0 and 1. """

    file_name = StringProperty("")
    """ The file name of the currently playing track """

    app = ObjectProperty()

    playlist = ObjectProperty()
    """ Reference to the Playlist object. """

    prune = True
    """ If set to true, remove files from the playlist once played. """

    store = ObjectProperty(StoreFactory.get())

    def __init__(self, **kwargs):
        """ Initialize the screens and the screen manager """
        config = kwargs.pop("config")
        self.prune = config["prune"]
        super().__init__(**kwargs)
        self.zenplayer = ZenPlayer(ctrl=self)
        self.playlist = Playlist(self.store)
        self.library = Library(config)
        self.advance = True

        if environ.get("KIVY_AUDIO", "") == "vlcplayer":
            register_vlc()

        if config["enable_hotkeys"]:
            HotKeyHandler.add_bindings(self)
        if config.get("enable_firebase", True):
            self.now_playing = NowPlaying()
            self.bind(state=lambda *args: self.now_playing.write_to_db(self))

        self.kb_handler = KeyHandler(self)
        self.sound = None
        Clock.schedule_interval(self._update_progress, 1/5)

        self._restore_state()

    def _restore_state(self):
        """ Load the state when previously exited if possible. """
        if "state" in self.store.keys():
            state = self.store.get("state")
            self.position = state["position"]
            self.volume = state["volume"]
            self.state = state["state"]

    def _set_sound(self):
        """
        Set and return a new sound from the SoundLoader, being sure to remove
        and create binding as appropraite
        """
        if self.sound is not None:
            self.sound.unbind(state=self.set_state)
            self.sound.stop()
        self.file_name = self.playlist.get_current_file()
        self.sound = SoundLoader.load(self.file_name)

        if self.sound is not None:
            self.sound.bind(state=self.set_state)
            self.sound.volume = self.volume
        return self.sound

    def set_state(self, _widget, value):
        """
        Set the state of the currently playing track. This is the callback
        fired when the media player encounters the end of track.
        """
        Logger.info("State changed to %s", value)
        if value == "stop" and self.state not in ["Stopped", "Paused"]:
            self.stop()
            if self.advance:
                self.play_next()

    def on_state(self, _widget, value):
        """ React to the change of state event """
        Logger.debug("controller.py: Entering on_state. value=%s", value)
        if value == "Playing":
            if self.sound is None:
                sound = self._set_sound()
                if sound:
                    sound.play()
                    self.set_position(self.position)
            else:
                self.sound.play()
        elif value == "Stopped" and self.sound:
            self.sound.stop()
            self.stop()
        elif value == "Paused" and self.sound:
            self.sound.stop()

    def open_in_browser(self):
        """Open a link to the React app in a browser."""

        import webbrowser
        webbrowser.open("http://127.0.0.1:9001/static/index.html")

    def _update_progress(self, _dt):
        """ Update the progressbar  """
        if self.sound and self.sound.state == "play":
            pos = self.sound.get_pos()
            length = self.sound.length
            if length > 0:
                self.time_display = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
                self.position = pos / length

    def on_file_name(self, _widget, value):
        """ Respond to the change of file name and set the info fields."""
        parts = value.split(sep)
        if len(parts) > 2:
            self.track = parts[-1]
            self.album = parts[-2]
            self.artist = parts[-3]
            self.cover = self.library.get_cover_path(self.artist, self.album)
            try:
                Window.set_icon(self.cover)
            except Exception as e:
                Logger.warning('Failed to set cover. Error %s', repr(e))
            Logger.info(
                "Track change: %s: %s - %s",
                self.artist, self.album, self.track)

    def volume_up(self):
        """ Turn the volume up """
        self.volume += 0.025

    def volume_down(self):
        """ Turn the volume down """
        self.volume -= 0.025

    def on_volume(self, _widget, value):
        """ Set the volume of the currently playing sound """
        volume = self.volume = abs(value) % 1.0 if value < 1 else 1
        if self.sound is not None:
            self.sound.volume = volume

    def move_forward(self):
        """ Move the current playing time 5s forward """
        pos = self.sound.get_pos()
        length = self.sound.length
        if length >= pos + 5:
            self.sound.seek(pos + 5)

    def move_backward(self):
        """ Move the current playing time 5s backward """
        pos = self.sound.get_pos()
        if pos > 5:
            self.sound.seek(pos - 5)

    def play_index(self, index):
        """
        Play the track with the specified playlist index
        """
        self.stop()
        self.playlist.current = index
        self.position = 0
        self._set_sound()
        self.play_pause()

    def remove_index(self, index):
        """
        Remove the track with the specified playlist index
        """
        self.playlist.remove_index(index)

    def play_pause(self):
        """ Play or pause the currently playing track """
        if self.state == "Playing":
            self.state = "Paused"
        else:
            self.state = "Playing"

    def add_random_album(self):
        """ Add a random album to the playlist """
        artist, album = self.library.get_random_album()
        self.playlist.add_files(self.library.get_path(artist, album))

    def play_random_album(self):
        """ Play a random album, replacing the playlist """
        self.stop()
        artist, album = self.library.get_random_album()
        self.playlist.add_files(
            self.library.get_path(artist, album), "replace")
        self.play_index(0)

    def play_next(self):
        """ Play the next track in the playlist. """
        self.advance = False
        self.stop()
        self.playlist.move_next(self.prune)
        if len(self.playlist.queue) == 0:
            self.add_random_album()
        self._set_sound()
        self.position = 0
        self.play_pause()
        self.advance = True

    def play_previous(self):
        """ Play the previous track in the playlist. """
        self.advance = False
        self.stop()
        self.position = 0
        self.playlist.move_previous()
        self._set_sound()
        self.play_pause()
        self.advance = True

    def set_position(self, value):
        """
        Set the playing position to the specified value, where value is  a
        fraction between 0 and 1.
        """
        sound = self.sound
        if sound and sound.length:
            sound.seek(value * sound.length)

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self.store)
        self.store.put("state", volume=self.volume, position=self.position,
                       state=self.state)

    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        self.position = 0.0
        self.state = "Stopped"
        self.advance = True

    def quit(self):
        """ Close the application """
        Logger.debug("controller.py: Entering quit. About to save.")
        self.save()
        self.stop()
        Clock.schedule_once(lambda dt: self.app.stop())
