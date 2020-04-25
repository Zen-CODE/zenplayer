from components.sound import Sound
from kivy.properties import (NumericProperty, ObjectProperty, StringProperty,
                             OptionProperty)
from kivy.event import EventDispatcher
from kivy.clock import Clock
from os import sep
from components.keyboard_handler import KeyHandler
from components.hotkey_handler import HotKeyHandler
from components.library import Library
from components.playlist import Playlist
from components.store import StoreFactory
from kivy.logger import Logger
from components.paths import rel_to_base
from kivy.core.window import Window
from ui.widgets.zenplayer import ZenPlayer


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
    state = OptionProperty("", options=["stopped", "paused", "playing", ""])
    prev_state = None

    position = NumericProperty(0.0)
    """ Position is the track as a fraction between 0 and 1. """

    # The following is used to trigger the above
    file_name = StringProperty("")

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
        self.library = Library()
        self.advance = True

        self.zenplayer.show_screen("Playing")

        if config["enable_hotkeys"]:
            HotKeyHandler.add_bindings(self)
        self.kb_handler = KeyHandler(self)
        self.sound = Sound()
        self.sound.bind(state=self.set_state)
        Clock.schedule_interval(self._update_progress, 1/5)

        self._restore_state()

    def _restore_state(self):
        """ Load the state when previously exited if possible. """
        if "state" in self.store.keys():
            state = self.store.get("state")
            self.position = state["position"]
            self.volume = state["volume"]
            self.state = state["state"]

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
        Logger.debug(f"controller.py: Entering on_state. value={value}")
        if value == "playing":
            if self.sound.state == "playing":
                self.sound.stop()
            self.file_name = self.playlist.get_current_file()
            if self.file_name:
                self.sound.play(self.file_name, self.volume, self.position)
        elif value == "stopped":
            self.sound.stop()
        elif value == "paused" and self.prev_state is not None:
            # If the prev_state is None, we have just restored state on start
            self.position, _length = self.sound.get_pos_length()
            self.sound.pause()

        self.prev_state = value

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
            Window.set_icon(self.cover)

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

    def remove_index(self, index):
        """
        Remove the track with the specified playlist index
        """
        self.playlist.remove_index(index)

    def play_pause(self):
        """ Play or pause the currently playing track """
        if self.state == "playing":
            self.state = "paused"
        else:
            self.state = "playing"

    def add_random_album(self):
        """ Add a random album to the playlist """
        artist, album = self.library.get_random_album()
        self.playlist.add_files(self.library.get_path(artist, album))

    def play_next(self):
        """ Play the next track in the playlist. """
        self.advance = False
        self.stop()
        self.playlist.move_next(self.prune)
        if len(self.playlist.queue) == 0:
            self.add_random_album()

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
        self.playlist.save(self.store)
        self.store.put("state", volume=self.volume, position=self.position,
                       state=self.state)

    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        self.position = 0.0
        self.state = "stopped"
        self.advance = True

    def quit(self):
        """ Close the application """
        Logger.debug("controller.py: Entering quit. About to save.")
        self.save()
        self.stop()
        Clock.schedule_once(lambda dt: self.app.stop())
