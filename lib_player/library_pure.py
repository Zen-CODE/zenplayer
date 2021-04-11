"""
This module houses the Zen Music Library class
"""
from os.path import expanduser, join, isdir, exists
from os import listdir
from random import choice


class Library:
    """
    Present a thin layer over the file system as a music library based on file
    name conventions.
    """
    def __init__(self):
        super().__init__()
        self.lib_path = expanduser("~/Music")

    @staticmethod
    def _safe_listdir(direc):
        """
        Return a list of folders in the given directory.

        This function is mainly to simplify error handling and filtering of
        directory listings.
        """
        if exists(direc):
            return [name for name in listdir(direc)
                    if isdir(join(direc, name))]
        return []

    def get_artists(self):
        """
        Return a list of artist available in this collection.
        """
        contents = [name for name in listdir(self.lib_path)
                    if isdir(join(self.lib_path, name))]
        return sorted(contents)

    def get_albums(self, artist):
        """
        Return a list of albums for the specified artist.
        """
        _path = join(self.lib_path, artist)
        contents = Library._safe_listdir(_path)
        return sorted(contents)

    def get_path(self, artist=None, album=None):
        """
        Return the path to the relevant folder. If niether album nor artist
        is specified, the root of the music library is returned.
        """
        if artist and album:
            return join(self.lib_path, artist, album)
        if artist:
            return join(self.lib_path, artist)
        return self.lib_path

    def get_random_album(self):
        """
        Choose and return a random album, returning the artist and album as
        a tuple.
        """
        artist = choice(self.get_artists())
        album = choice(self.get_albums(artist))
        return artist, album


if __name__ == "__main__":
    print(Library().get_artists())
