"""
This module houses the screen displaying track information
"""

from pathlib import Path
from threading import Thread
from typing import Any, Optional
import webbrowser
from urllib.parse import quote
from requests import get
from mutagen import File

from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.uix.label import Label

from components.meta import Metadata
from ui.screens.zenscreen import ZenScreen


def get_header_label(text: str) -> Label:
    return Label(
        text=f"[color=#00DD00][b]{text}[/b][/color]",
        markup=True,
        size_hint_y=None,
        height=30,
    )


def get_label(text: str) -> Label:
    return Label(text=text, size_hint_y=None, height=25, markup=True)


class InfoScreen(ZenScreen):
    """
    The main screen that shows what's currently playing
    """

    filename = StringProperty(None, allownone=True)
    """ Display the track with the given filename. If set to anything Falsy,
    the current track will be displayed and updated on track changing. We set
    to None so an empty string still trigger on `on_filename` event.
    """

    units: dict[str, str] = {"length": "s", "bitrate": " kbps", "sample_rate": " hz"}
    """
    Defines the list of unit suffixes to be used when displaying track
    metadata.
    """

    def _show_current_track(self, *_args: Any) -> None:
        """Display the currently playing track in the playlist"""
        file_name = self.ctrl.playlist.get_current_file()
        if file_name:
            self._show(file_name)

    def on_filename(self, _widget: Any, filename: Optional[str]) -> None:
        """Respond to the changing of the filename"""
        if filename:
            Logger.info("InfoScreen: Unbinding. Set to fixed track.")
            self.ctrl.playlist.unbind(current=self._show_current_track)
            self.ctrl.playlist.unbind(queue=self._show_current_track)
            Clock.schedule_once(lambda dt: self._show(filename))
        else:
            Logger.info("InfoScreen: Binding to the current track.")
            Clock.schedule_once(self._show_current_track)
            self.ctrl.playlist.bind(current=self._show_current_track)
            self.ctrl.playlist.bind(queue=self._show_current_track)

    def _show(self, filename: str) -> None:
        """Show all the details on the given filename"""
        self._show_art(filename)

        sv = self.ids["info_scroll"]
        sv.clear_widgets()
        sv.add_widget(Label(text="", size_hint_y=None, height=10))
        self._show_info(filename, sv)
        self._show_meta(filename, sv)
        self._show_tags(filename, sv)
        sv.add_widget(Label(text="", size_hint_y=None, height=10))

    def _show_tags(self, filename: str, sv: Any) -> None:
        """Populate the audio tag track info (ID3, Vorbis, FLAC, MP4, etc.)"""
        try:
            audio = File(filename, easy=True)
            if audio and audio.tags:
                display_list = [
                    f"{key.title()}: [i]{value[0] if isinstance(value, list) and value else value}[/i]"
                    for key, value in sorted(audio.tags.items())
                ]
                if display_list:
                    sv.add_widget(get_header_label(text="Audio Tags"))
                    for item in display_list:
                        sv.add_widget(get_label(text=item))
        except Exception as e:
            Logger.debug("InfoScreen: Unable to load audio tags: %s", e)

    def _show_info(self, filename: str, sv: Any) -> None:
        """Populate the track info"""
        data = self.ctrl.playlist.get_info(filename=filename)
        data_list = [
            f"{key.title().replace('_', ' ')} : [i]{data[key]}[/i]"
            for key in ["artist", "album", "track_name", "track_number"]
        ]
        sv.add_widget(get_header_label(text="Track Info"))
        for item in data_list:
            sv.add_widget(get_label(text=item))

    def _show_meta(self, filename: str, sv: Any) -> None:
        """Populate the technical file metadata"""
        meta = Metadata.get(filename)
        meta_list = [
            f"{key.title().replace('_', ' ')}: [i]{self.format_meta_value(key, value)}[/i]"
            for key, value in meta.items()
        ]
        sv.add_widget(get_header_label(text="File Metadata"))
        for item in meta_list:
            sv.add_widget(get_label(text=item))

    @staticmethod
    def format_meta_value(key: str, value: Any) -> str:
        """Return the prettily formatted string for the given key"""
        if key == "length":
            val_f = float(value)
            return f"{int(val_f / 60.0)}m {int(val_f % 60):02d}s"
        unit = InfoScreen.units.get(key, "")
        return f"{value}{unit}"

    def _show_art(self, filename: str) -> None:
        """Populate the track cover art"""
        parts = Path(filename).parts
        if len(parts) >= 3:
            self.ids["image"].source = self.ctrl.library.get_cover_path(
                parts[-3], parts[-2]
            )
        else:
            self.ids["image"].source = self.ctrl.library.get_cover_path("", "")

    def show_artist_info(self) -> None:
        """Open a link in wikipedia showing the artist info in a background thread."""
        artist = self.ctrl.playlist.get_current_info().get("artist")
        if not artist or artist == "-":
            Logger.warning("No suitable artist link found for %s.", artist)
            return

        def _fetch_and_open() -> None:
            url = Wikipedia.get_artist_url(artist)
            if url:
                webbrowser.open(url)
            else:
                Logger.warning("No suitable artist link found for %s.", artist)

        Thread(target=_fetch_and_open, daemon=True).start()


class Wikipedia:
    """
    Class for handling Wikipedia queries.
    """

    @staticmethod
    def get_artist_url(artist: str) -> Optional[str]:
        """Return the most likely URL for the specified artist"""
        url = (
            f"https://en.wikipedia.org/w/api.php?format=json&action=query&"
            f"list=search&srsearch={quote(artist + ' music band')}"
        )
        try:
            resp = get(url, timeout=5)
            if resp.status_code == 200:
                results = resp.json().get("query", {}).get("search", [])
                if results:
                    page_id = results[0]["pageid"]
                    return f"https://en.wikipedia.org/?curid={page_id}"
            else:
                Logger.error("Error returned from Wikipedia: %s", resp)
        except Exception as e:
            Logger.error("Unable to query Wikipedia: %s", e)
        return None
