from os import listdir
from os.path import expanduser
from pathlib import Path
from random import choice
from functools import lru_cache
from zenmpdcore import MPDCore, MPDClient


MUSIC_DIR = "/home/richard/Zen/Music/"


class ZenMPD(MPDCore):
    version: str = "0.3"

    @staticmethod
    def _get_library_files(folder: str, existing: list | None = None) -> list[str]:
        top_level = bool(existing is None)
        files = [] if top_level else existing
        for f in sorted(listdir(folder), reverse=False):
            file_path = Path(f"{folder}/{f}")
            if file_path.is_dir():
                ZenMPD._get_library_files(str(file_path), existing=files)
            else:
                ext = f.split(".")[-1].lower()
                if ext in ["mp3", "flac", "wav", "m4a", "wma", "ogg"]:
                    files.append(str(file_path))
        if top_level:
            return [fname.replace(MUSIC_DIR, "") for fname in files]

    @staticmethod
    def add(folder: str):
        client = ZenMPD._ensure_client()
        for lib_file in ZenMPD._get_library_files(folder):
            client.add(lib_file)

    @staticmethod
    def replace(folder: str):
        client = ZenMPD._ensure_client()
        client.stop()
        client.clear()
        for lib_file in ZenMPD._get_library_files(folder):
            client.add(lib_file)
        client.play(0)

    @staticmethod
    def play():
        client = ZenMPD._ensure_client()
        status = client.status()
        if status.get("state") == "pause":
            client.pause(0)
        elif status.get("state") != "play":
            client.play(int(status.get("song", 0)))

    @staticmethod
    def playpause():
        client = ZenMPD._ensure_client()
        status = client.status()
        match status.get("state"):
            case "play":
                client.pause(1)
            case "pause":
                client.pause(0)
            case _:
                client.play(int(status.get("song", 0)))

    @staticmethod
    def previous():
        client = ZenMPD._ensure_client()
        pos = int(client.status().get("song", 0))
        client.play(max(pos - 1, 0))

    @staticmethod
    def next():
        client = ZenMPD._ensure_client()
        status = client.status()
        pos = int(status.get("song", -1))
        if pos + 1 < int(status.get("playlistlength", 0)):
            client.play(pos + 1)

    @staticmethod
    def volup():
        client = ZenMPD._ensure_client()
        status = client.status()
        volume = int(status.get("volume", 0))
        client.setvol(min(volume + 5, 100))

    @staticmethod
    def voldown():
        client = ZenMPD._ensure_client()
        status = client.status()
        volume = int(status.get("volume", 0))
        client.setvol(max(volume - 5, 0))

    @lru_cache
    @staticmethod
    def music_directory() -> str | None:
        """
        Return the MPD config music_directory or None
        Note:
            This assumes the MPDClient is running locally as this is intended
            as a local music player.
        """
        music_path: Path = Path(expanduser("~/.config/mpd/mpd.conf"))
        if not music_path.exists():
            music_path = Path("/etc/mpd.conf")
            if not music_path.exists():
                return None

        for line in music_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("music_directory"):
                return line.split('"', 2)[1]

        return None

    @staticmethod
    def _choose_random_album(client: MPDClient) -> str | None:
        all_files = client.listall("/")
        chosen, count = None, 0
        while count < 100 and not chosen:
            candidate = choice(all_files)
            if file_name := candidate.get("file"):
                test_chosen = file_name.split("/")
                if len(test_chosen) > 1:
                    chosen = MUSIC_DIR + "/".join(test_chosen[:-1])
            count += 1
        return chosen

    @staticmethod
    def playrandomalbum():
        client = ZenMPD._ensure_client()
        if chosen := ZenMPD._choose_random_album(client):
            files = ZenMPD._get_library_files(chosen)
            if files:
                client.stop()
                client.clear()
                for file_ in files:
                    client.add(file_)
                client.play(0)
            else:
                raise ValueError(f"Not files found to load from: {chosen}")

    @staticmethod
    def addrandomalbum():
        client = ZenMPD._ensure_client()
        if chosen := ZenMPD._choose_random_album(client):
            for file_ in ZenMPD._get_library_files(chosen):
                client.add(file_)

    @staticmethod
    def _get_folder_art(file_path: str) -> str | None:
        folder_path = Path(MUSIC_DIR + file_path).parent
        for file_name in folder_path.iterdir():
            if file_name.is_file() and file_name.name.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                return str(file_name)
        return None

    @staticmethod
    def nowplaying() -> dict | str | None:
        client = ZenMPD._ensure_client()
        status = client.status()
        song = client.currentsong()
        file_ = song.get("file", "")
        if file_ and Path(file_).exists():
            albumart = client.albumart(file_)
        else:
            albumart = ZenMPD._get_folder_art(file_)
        return status, song, albumart

    @staticmethod
    def playlist() -> tuple[list[dict], str | None]:
        client = ZenMPD._ensure_client()
        playlist_info = client.playlistinfo()
        current_id = client.currentsong().get("id")
        return playlist_info, current_id

    @staticmethod
    def disconnect_client():
        """Initialise the connected client"""
        if ZenMPD.client is not None:
            try:
                ZenMPD.client.close()
                ZenMPD.client.disconnect()
            except:  # noqa BL001
                pass
            ZenMPD.client = None
