"""
This module houses the Zen Music Library class
"""
from os.path import expanduser, join, isdir, exists
from os import listdir


class Library:
    """
    Present a thin layer over the file system as a music library based on file
    name conventions.
    """
    def __init__(self):
        super().__init__()
        self.lib_path = expanduser("~/Music")

    @staticmethod
    def _safe_listdir(direc, filter):
        """
        Return a list of items in the given directory if then filer function
        returns True given the filename.

        This function is mainly to simplify error handling and filtering of
        directory listings.
        """
        if exists(direc):
            return [name for name in listdir(direc)
                    if isdir(join(direc, name))]
        else:
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
        contents = self._safe_listdir(_path, isdir)
        return sorted(contents)
