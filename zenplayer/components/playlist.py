from os import sep, path
from kivy.event import EventDispatcher
from kivy.properties import (  # pylint: disable=no-name-in-module
    NumericProperty,
    ListProperty,
)
from components.filedrop import FileDrop
from zenmpd import ZenMPD, MUSIC_DIR


class Playlist(EventDispatcher):
    """
    Holds the current playlist, backed natively by MPD via ZenMPD.
    """

    current = NumericProperty(0)
    """ The index of the currently playing track in the queue. """

    queue = ListProperty([])
    """
    Contains a list of dictionaries with the following keys:
        * text: Used to display the track in the playlist
        * filename: Full path to the audio file
        * id: MPD song id
        * pos: MPD position
    """

    def __init__(self, store=None, **kwargs):
        super().__init__(**kwargs)
        self.file_drop = FileDrop(self)
        self.sync()

    @staticmethod
    def to_rel_path(file_path: str) -> str:
        """Strip MUSIC_DIR from file_path for MPD insertion."""
        if file_path.startswith(MUSIC_DIR):
            return file_path[len(MUSIC_DIR) :]
        if file_path.startswith(MUSIC_DIR):
            return file_path[len(MUSIC_DIR) :]
        return file_path.lstrip("/")

    @staticmethod
    def to_abs_path(rel_path: str) -> str:
        """Prepend MUSIC_DIR to rel_path for local retrieval."""
        if not rel_path:
            return ""
        if path.isabs(rel_path):
            return rel_path
        return path.join(MUSIC_DIR, rel_path)

    def sync(self):
        """Synchronize the playlist queue and current index with MPD."""
        try:
            pl_info, current_id = ZenMPD.playlist()
        except Exception:
            return

        new_queue = []
        current_idx = 0
        for idx, item in enumerate(pl_info):
            abs_path = self.to_abs_path(item.get("file", ""))
            new_queue.append(
                {
                    "text": self.get_text(abs_path),
                    "filename": abs_path,
                    "id": item.get("id"),
                    "pos": idx,
                }
            )
            if current_id is not None and str(item.get("id")) == str(current_id):
                current_idx = idx

        self.queue = new_queue
        self.current = current_idx

    def get_current_file(self):
        """Returns the filename of the current audio file."""
        try:
            song = ZenMPD.get_currentsong()
            if song and "file" in song:
                return self.to_abs_path(song["file"])
        except Exception:
            pass
        if len(self.queue) > self.current:
            return self.queue[self.current]["filename"]
        return ""

    def get_current_info(self):
        """Return a dictionary of information on the current track."""
        return self.get_info(filename=self.get_current_file())

    @staticmethod
    def get_text(file_):
        """
        Return the text to display on the playlist given the specified file.
        """
        parts = file_.split(sep)
        return " - ".join(parts[-3:])

    def add_files(self, file_folder, mode="add"):
        """
        Add the selected album or track to the MPD playlist. *mode* can be one of
        * "add" - add to the end of the playlist
        * "replace" - clear the existing playlist and add the files
        * "insert" - insert at the beginning of the playlist
        * "next" - insert directly after the currently playing track
        * "next_album" - insert directly after the current album
        """
        try:
            client = ZenMPD._ensure_client()
        except Exception:
            return

        if path.isdir(file_folder):
            rel_files = ZenMPD._get_library_files(file_folder)
        elif path.isfile(file_folder):
            rel_files = [self.to_rel_path(file_folder)]
        else:
            rel_files = []

        if not rel_files:
            return

        if mode == "replace":
            client.stop()
            client.clear()
            for f in rel_files:
                client.add(f)
            client.play(0)
        elif mode == "add":
            for f in rel_files:
                client.add(f)
        elif mode == "insert":
            for i, f in enumerate(rel_files):
                client.addid(f, i)
        elif mode == "next":
            status = client.status()
            cur_pos = int(status.get("song", 0))
            for i, f in enumerate(rel_files):
                client.addid(f, cur_pos + 1 + i)
        elif mode == "next_album":
            status = client.status()
            cur_pos = int(status.get("song", 0))
            pl_info, _ = ZenMPD.playlist()
            target_pos = cur_pos + 1
            if pl_info and 0 <= cur_pos < len(pl_info):
                cur_album_dir = path.dirname(pl_info[cur_pos].get("file", ""))
                while (
                    target_pos < len(pl_info)
                    and path.dirname(pl_info[target_pos].get("file", ""))
                    == cur_album_dir
                ):
                    target_pos += 1
            for i, f in enumerate(rel_files):
                client.addid(f, target_pos + i)

        self.sync()

    def clear_files(self):
        """Clear the existing playlist."""
        try:
            client = ZenMPD._ensure_client()
            client.stop()
            client.clear()
        except Exception:
            pass
        self.sync()

    def move_next(self):
        """Move to the next track."""
        ZenMPD.next()
        self.sync()

    def move_previous(self):
        """Move to the previous track."""
        ZenMPD.previous()
        self.sync()

    def remove_index(self, index):
        """Remove the specified track from the queue."""
        try:
            client = ZenMPD._ensure_client()
            client.delete(index)
        except Exception:
            pass
        self.sync()

    def set_index(self, index):
        """Set the currently selected track to the one specified by the index."""
        try:
            client = ZenMPD._ensure_client()
            client.play(index)
        except Exception:
            pass
        self.sync()

    def save(self, store=None):
        """Playlist persistence is handled natively by MPD."""
        pass

    def get_info(self, filename=None, index=None):
        """
        Return a dictionary containing the track information with keys:
            * artist
            * album
            * track
            * track_name
            * track_number
        """

        def number_name(_basename):
            not_ext = _basename[0 : _basename.rfind(".")]
            parts = not_ext.split("-")
            try:
                return str(int(parts[0])), "-".join(parts[1:]).strip()
            except ValueError:
                return "-", not_ext

        try:
            if index is not None and index < len(self.queue):
                parts = self.queue[index]["filename"].split(sep)
            elif filename:
                parts = filename.split(sep)
            else:
                parts = []
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
