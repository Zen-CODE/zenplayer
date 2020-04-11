"""
This module houses teh API interface for the Zenlibrary
"""
from webserver.api.zenapibase import ZenAPIBase
from os.path import expanduser, join, isdir, exists
from os import listdir
from flask import request


class ZenLibrary(ZenAPIBase):
    """
    Present an API interface for interaction with the Zenplaylist object.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        ---
        tags:
            - ZenLibrary
        responses:
            200:
                description: Return the state of the current track.
            schema:
                type: array
                items:
                    string
        """
        contents = [name for name in listdir(self.lib_path)
                    if isdir(join(self.lib_path, name))]
        return self.resp_from_data([name for name in sorted(contents)])

    def get_albums(self):
        """
        Return a list of albums for the specified artist.
        ---
        tags:
            - ZenLibrary
        parameters:
            - name: artist
              in: query
              type: string
        responses:
            200:
                description: Return the state of the current track.
            schema:
                type: array
                items:
                    string
        """
        artist = request.args.get("artist")
        if artist:
            _path = join(self.lib_path, artist)
            contents = self._safe_listdir(_path, isdir)
            if contents:
                return self.resp_from_data([name for name in sorted(contents)])
            else:
                return self.resp_from_data(
                    {"message": f"No album found for {artist}"}, 400)
        return self.resp_from_data({"message": "No artist specified"}, 400)
