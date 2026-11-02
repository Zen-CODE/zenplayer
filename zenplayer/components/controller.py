from os import sep
import webbrowser
from kivy.properties import (  # pylint: disable=no-name-in-module
    NumericProperty,
    ObjectProperty,
    StringProperty,
    OptionProperty,
)
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.window import Window

from components.keyboard_handler import KeyHandler
from components.hotkey_handler import HotKeyHandler
from components.library import Library
from components.playlist import Playlist
from components.store import StoreFactory
from components.paths import rel_to_base
from components.config import Config
from ui.widgets.zenplayer import ZenPlayer
from zenmpd import ZenMPD


class Controller(EventDispatcher):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays using the MPD backend.
    """

    volume = NumericProperty(1.0)
    artist = StringProperty("-")
    album = StringProperty("-")
    track = StringProperty("-")
    cover = StringProperty(rel_to_base("images", "zencode.png"))
    time_display = StringProperty("-")
    state = OptionProperty("", options=["Stopped", "Paused", "Playing", ""])

    position = NumericProperty(0.0)
    """ Position in the track as a fraction between 0 and 1. """

    file_name = StringProperty("")
    """ The file name of the currently playing track """

    app = ObjectProperty()

    playlist = ObjectProperty()
    """ Reference to the Playlist object. """

    store = ObjectProperty()

    def __init__(self, **kwargs):
        """Initialize the screens and the screen manager"""
        config = kwargs.pop("config")
        super().__init__(**kwargs)
        self.store = StoreFactory.get()
        self.zenplayer = ZenPlayer(ctrl=self)
        self.playlist = Playlist(self.store)
        self.library = Library(config)
        self._was_playing = False

        if config.get("enable_hotkeys", False):
            HotKeyHandler.add_bindings(self)

        self.kb_handler = KeyHandler(self)
        Clock.schedule_interval(self._update_progress, 1 / 5)

        self._sync_initial_state()

    def _sync_initial_state(self):
        """Sync initial state from MPD if available."""
        try:
            status = ZenMPD.get_status()
            if "volume" in status and status["volume"] != "-1":
                self.volume = float(status["volume"]) / 100.0
            mpd_state = status.get("state")
            if mpd_state == "play":
                self.state = "Playing"
                self._was_playing = True
            elif mpd_state == "pause":
                self.state = "Paused"
            else:
                self.state = "Stopped"

            song = ZenMPD.get_currentsong()
            if song and "file" in song:
                self.file_name = self.playlist.to_abs_path(song["file"])
        except Exception as e:
            Logger.warning("Controller: Initial MPD sync failed: %s", e)

    def _update_progress(self, _dt):
        """Update player state and progress from MPD"""
        try:
            status = ZenMPD.get_status()
        except Exception:
            return

        mpd_state = status.get("state")
        if mpd_state == "play":
            self.state = "Playing"
        elif mpd_state == "pause":
            self.state = "Paused"
        else:
            self.state = "Stopped"

        if mpd_state in ["play", "pause"]:
            pos = float(status.get("elapsed", 0.0))
            length = float(status.get("duration", 0.0))
            if length > 0:
                self.time_display = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60), int(pos % 60), int(length / 60), int(length % 60)
                )
                self.position = pos / length
        else:
            self.position = 0.0
            self.time_display = "-"

        if "volume" in status and status["volume"] != "-1":
            try:
                v = float(status["volume"]) / 100.0
                if abs(self.volume - v) > 0.01:
                    self.volume = v
            except ValueError:
                pass

        try:
            song = ZenMPD.get_currentsong()
        except Exception:
            song = {}

        current_file = self.playlist.to_abs_path(song.get("file", "")) if song else ""
        if current_file and current_file != self.file_name:
            self.file_name = current_file
            self.playlist.sync()
        elif not current_file and self.file_name and mpd_state == "stop":
            self.file_name = ""

        # End of playlist detection: when it reaches the end, play random album
        if mpd_state == "stop" and self._was_playing:
            self._was_playing = False
            self.play_random_album()
        elif mpd_state == "play":
            self._was_playing = True

    def on_file_name(self, _widget, value):
        """Respond to the change of file name and set the info fields."""
        parts = value.split(sep)
        if len(parts) > 2:
            self.track = parts[-1]
            self.album = parts[-2]
            self.artist = parts[-3]
            self.cover = self.library.get_cover_path(self.artist, self.album)
            try:
                Window.set_icon(self.cover)
            except Exception as e:
                Logger.warning("Failed to set cover. Error %s", repr(e))
            Logger.info(
                "Track change: %s: %s - %s", self.artist, self.album, self.track
            )

    def open_in_browser(self):
        """Open a link to the React app in a browser."""
        config = Config.load("webserver.json")
        webbrowser.open(f"http://{config['host']}:{config['port']}/static/index.html")

    def volume_up(self):
        """Turn the volume up"""
        ZenMPD.volup()

    def volume_down(self):
        """Turn the volume down"""
        ZenMPD.voldown()

    def on_volume(self, _widget, value):
        """Set the volume of MPD"""
        volume = max(0.0, min(1.0, value))
        try:
            client = ZenMPD._ensure_client()
            client.setvol(int(volume * 100))
        except Exception:
            pass

    def move_forward(self):
        """Move the current playing time 5s forward"""
        try:
            client = ZenMPD._ensure_client()
            client.seekcur("+5")
        except Exception:
            pass

    def move_backward(self):
        """Move the current playing time 5s backward"""
        try:
            client = ZenMPD._ensure_client()
            client.seekcur("-5")
        except Exception:
            pass

    def set_position(self, value):
        """
        Set the playing position to the specified value, where value is a
        fraction between 0 and 1.
        """
        try:
            status = ZenMPD.get_status()
            duration = float(status.get("duration", 0.0))
            if duration > 0:
                target = int(value * duration)
                client = ZenMPD._ensure_client()
                client.seekcur(target)
        except Exception:
            pass

    def play_index(self, index):
        """Play the track with the specified playlist index."""
        try:
            client = ZenMPD._ensure_client()
            client.play(index)
        except Exception:
            pass

    def remove_index(self, index):
        """Remove the track with the specified playlist index."""
        self.playlist.remove_index(index)

    def play_pause(self):
        """Play or pause the currently playing track"""
        ZenMPD.playpause()

    def play_next(self):
        """Play the next track in the playlist, or random album if at end."""
        try:
            status = ZenMPD.get_status()
            pos = int(status.get("song", -1))
            pl_len = int(status.get("playlistlength", 0))
            if pos + 1 >= pl_len or pl_len == 0:
                self.play_random_album()
            else:
                ZenMPD.next()
        except Exception:
            self.play_random_album()

    def play_previous(self):
        """Play the previous track in the playlist."""
        ZenMPD.previous()

    def play_random_album(self):
        """Play a random album, replacing the playlist"""
        ZenMPD.playrandomalbum()
        self.playlist.sync()

    def add_random_album(self):
        """Add a random album to the playlist"""
        ZenMPD.addrandomalbum()
        self.playlist.sync()

    def stop(self):
        """Stop any playing audio"""
        self._was_playing = False
        ZenMPD.stop()
        self.position = 0.0
        self.state = "Stopped"

    def save(self):
        """Save the state of the playlist and volume."""
        self.playlist.save(self.store)

    def quit(self):
        """Close the application"""
        Logger.debug("controller.py: Entering quit. About to save.")
        self.save()
        self.stop()
        Clock.schedule_once(lambda dt: self.app.stop())
