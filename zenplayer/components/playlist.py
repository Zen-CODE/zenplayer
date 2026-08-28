"""
This module houses the Playlist class for ZenPlayer, managing the track queue
and VLC's MediaListPlayer for seamless gapless playback.
"""

from os import listdir, sep
from os.path import exists, isdir, join
from typing import Any, Optional, TypedDict
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.properties import (
    ListProperty,
    NumericProperty,
)
from vlc import Event, EventType, Instance, Media, MediaList, MediaListPlayer

from components.filedrop import FileDrop
from components.filesystemextractor import FileSystemExtractor


class PlaylistItem(TypedDict):
    """Represents a single track entry in the playlist queue."""

    filename: str
    text: str


class TrackInfo(TypedDict):
    """Represents metadata extracted for a track."""

    artist: str
    album: str
    track: str
    track_name: str
    track_number: str


class Playlist(EventDispatcher):
    """
    Holds the current playlist class and coordinates VLC MediaListPlayer
    for gapless playback between song transitions.
    """

    current: int = NumericProperty(0)
    """ The index of the currently playing track in the queue. """

    queue: list[PlaylistItem] = ListProperty([])
    """
    Contains a list of dictionaries with the following keys:
        * text: Used to display the track in the playlist
        * filename: Full path to the audio file
    """

    instance: Instance
    media_list: MediaList
    media_list_player: MediaListPlayer
    file_drop: FileDrop

    def __init__(self, store: Any, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.instance = Instance()
        self.media_list_player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new()
        self.media_list_player.set_media_list(self.media_list)
        self._attach_events()
        self._load(store)
        self.file_drop = FileDrop(self)

    def _attach_events(self) -> None:
        """Attach event listeners for VLC MediaListPlayer events."""
        event_manager = self.media_list_player.event_manager()
        event_manager.event_attach(
            EventType.MediaListPlayerNextItemSet,
            self._on_next_item_set,
        )

    @mainthread
    def _on_next_item_set(self, _event: Event) -> None:
        """Handle the VLC MediaListPlayer NextItemSet event on the main thread."""
        media_player = self.media_list_player.get_media_player()
        if media_player is not None:
            media = media_player.get_media()
            if media is not None:
                index: int = self.media_list.index_of_item(media)
                if 0 <= index < len(self.queue) and index != self.current:
                    self.current = index
                media.release()
            media_player.release()

    def _load(self, store: Any) -> None:
        """Initialize and load previous state"""
        # See if there is an existing playlist to restore
        if store.exists("Playlist"):
            playlist_data: dict[str, Any] = store.get("Playlist")
            if "items" in playlist_data:
                items: dict[str, str] = playlist_data["items"]
                k: int = 1
                while "item" + str(k) in items:
                    item_path: str = items["item" + str(k)]
                    if exists(item_path):
                        self.add_files(item_path)
                    k += 1
            if "current" in playlist_data:
                self.current = playlist_data["current"]
            if self.current >= len(self.queue) - 1:
                self.current = 0

    def get_current_file(self) -> str:
        """Returns the filename of the current audio file."""
        if 0 <= self.current < len(self.queue):
            return self.queue[self.current]["filename"]
        return ""

    def get_current_info(self) -> TrackInfo:
        """Return a dictionary of information on the current track"""
        return self.get_info(index=self.current)

    @staticmethod
    def get_text(file_: str) -> str:
        """
        Return the text to display on the playlist given the specified file.
        """
        parts = file_.split(sep)
        return " - ".join(parts[-3:])

    def _get_index(self, mode: str) -> int:
        """Return the index of where to insert the files."""
        if len(self.queue) < 1:
            return 0

        if mode == "insert":
            return 0
        if mode == "next":
            return 1
        start: int = 1
        folder: str = "/".join(self.queue[0]["filename"].split("/")[:-1])
        while (
            start < len(self.queue) and self.queue[start]["filename"].find(folder) > -1
        ):
            start += 1
        return start

    def _add_files(self, file_folder: str, mode: str = "add") -> None:
        """
        Internal implementation of the addition, support recursion but
        extracted for once of setup in add_file
        """
        if isdir(file_folder):
            for f in sorted(
                listdir(file_folder),
                reverse=bool(mode in ["insert", "next", "next_album"]),
            ):
                self._add_files(join(file_folder, f), mode=mode)
        elif str("." + file_folder.split(".")[-1]) in FileSystemExtractor.music_types:
            item: PlaylistItem = {
                "filename": file_folder,
                "text": self.get_text(file_folder),
            }
            media: Media = self.instance.media_new(file_folder)
            if mode in ["insert", "next", "next_album"]:
                index: int = self._get_index(mode)
                self.queue.insert(index, item)
                self.media_list.insert_media(media, index)
            else:
                self.queue.append(item)
                self.media_list.add_media(media)
            media.release()

    def add_files(self, file_folder: str, mode: str = "add") -> None:
        """
        Add the selected album to the queue. *mode* can be one of
        * "add" - add to the end of the playlist
        * "replace" - clear the existing playlist and add the files
        * "insert" - insert the selected album at the beginning of the playlist
        * "next" - insert directly after the currently playing track
        * "next_album" - insert directly after the currently playing track
        """
        if mode == "replace":
            self.clear_files()
        self._add_files(file_folder, mode)

    def clear_files(self) -> None:
        """Clear the existing playlist"""
        self.queue = []
        self.current = 0
        self.media_list.release()
        self.media_list = self.instance.media_list_new()
        self.media_list_player.set_media_list(self.media_list)

    def move_next(self, prune: bool = False) -> None:
        """
        Move the selected track to the next. If *prune* is True, the
        current track is removed from the playlist.
        """
        if prune:
            if 0 <= self.current < len(self.queue):
                self.queue.pop(self.current)
                self.media_list.remove_index(self.current)
        else:
            self.current += 1

        if self.current + 1 > len(self.queue):
            self.current = 0

    def move_previous(self) -> None:
        """Move the selected track to the previous entry"""
        if self.current > 0:
            self.current -= 1

    def save(self, store: Any) -> None:
        """The playlist screen is being closed"""
        all_items: dict[str, str] = {}
        for k, item in enumerate(self.queue):
            all_items["item" + str(k + 1)] = item["filename"]
        store.put("Playlist", current=self.current, items=all_items)

    def set_index(self, index: int) -> None:
        """Set the currently selected track to the one specified by the index"""
        if 0 <= index < len(self.queue):
            self.current = index

    def remove_index(self, index: int) -> None:
        """Remove the specified track from the queue."""
        if 0 <= index < len(self.queue):
            self.queue.pop(index)
            self.media_list.remove_index(index)

    def get_info(
        self,
        filename: Optional[str] = None,
        index: Optional[int] = None,
    ) -> TrackInfo:
        """
        Return a dictionary containing the track information with the following
        keys:
            * artist
            * album
            * track
            * track_name
            * track_number

        """

        def number_name(_basename: str) -> tuple[str, str]:
            """
            Return a tuple of the number and name of the track where the
            *_basename* is the filename without the path.
            """
            not_ext = _basename[0 : _basename.rfind(".")]
            parts = not_ext.split("-")
            try:
                return str(int(parts[0])), "-".join(parts[1:]).strip()
            except ValueError:
                return "-", not_ext

        try:
            if index is None:
                if filename is None:
                    raise IndexError
                parts = filename.split(sep)
            else:
                parts = self.queue[index]["filename"].split(sep)
            number, name = number_name(parts[-1])
            return {
                "artist": parts[-3],
                "album": parts[-2],
                "track": parts[-1],
                "track_name": name,
                "track_number": number,
            }
        except IndexError:
            return {
                "artist": "-",
                "album": "-",
                "track": "-",
                "track_name": "-",
                "track_number": "-",
            }
