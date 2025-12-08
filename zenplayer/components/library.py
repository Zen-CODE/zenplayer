from os.path import join, expanduser, exists
from components.filesystemextractor import FileSystemExtractor as fse
from dataclasses import dataclass, field
from typing import List
from random import choice
from kivy.app import platform


@dataclass
class Track:
    name: str
    cover: str = ""


@dataclass
class Album:
    name: str
    tracks: List[Track] = field(default_factory=list)


class Library:
    """
    Class for fetching information about our music library. This information
    is built from the folder structure and filenames and used to populate a
    Pandas DataFrame for access and analysis.

    Args:
        config (dict): A dictionary with config. The following keys are used:
                       * `library_folder` - the path Music files.
    """

    def __init__(self, config):
        if platform == "android":
            path = "/storage/emulated/0/Music"
        else:
            path = expanduser(config.get("library_folder", "~/Zen/Music"))
        """ The fully expanded path to the music libary folder."""
        self.path = path

        self.artists = self._build_artist_dict(path) if exists(path) else {}
        """ A dictionary of `artist` / `Track` pairs."""

    @staticmethod
    def _choose_cover(covers):
        """Select a cover from the given list."""
        if covers:
            cover = covers[0]
            for image in covers[1:]:
                if image.find("cover") > -1:
                    cover = image
            return cover
        return ""

    @staticmethod
    def _build_artist_dict(path) -> dict:
        """Build the artist dictionary from the *path* folder."""

        artists = {}
        for artist in fse.get_dirs(path):
            artist_path = join(path, artist)
            for album in fse.get_dirs(artist_path):
                _tracks, _covers = fse.get_media(join(artist_path, album))
                if artist not in artists.keys():
                    artists[artist] = {}
                if album not in artists[artist].keys():
                    artists[artist][album] = []
                for track in _tracks:
                    artists[artist][album].append(
                        Track(name=track, cover=Library._choose_cover(_covers))
                    )
        return artists

    def get_artists(self):
        """Return a list of artists."""
        return list(self.artists.keys())

    def get_albums(self, artist):
        """Return a list of albums for the *artist*."""
        return list(self.artists[artist].keys())

    def get_cover_path(self, artist, album):
        """Return the album cover art for the given artist and album."""
        track = self.artists[artist][album][0]
        if track.cover:
            file_name = str(track.cover)
            return join(self.path, artist, album, file_name)
        return join(self.path, "default.png")

    def get_random_album(self):
        """Return a randomly selected artist and album."""
        artist = choice(list(self.artists.keys()))
        album = choice(list(self.artists[artist].keys()))
        return artist, album

    def get_tracks(self, artist, album):
        """
        Return the list of tracks on the specified album
        """
        return [track.name for track in self.artists[artist][album]]

    def get_path(self, artist, album):
        """
        Return the full path to the specified album. If the album does not
        exist, return an empty string.
        """
        path = join(self.path, artist, album)
        return path if exists(path) else ""

    def search(self, term):
        """Return the first instance of an artist or album with the text in."""
        for artist in self.artists.keys():
            for album in self.artists[artist].keys():
                if term.lower() in (artist + album).lower():
                    return {"artist": artist, "album": album}

        return {}
