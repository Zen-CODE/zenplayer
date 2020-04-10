"""
This module houses teh API interface for the Zenlibrary
"""
from webserver.api.zenapibase import ZenAPIBase
from os.path import expanduser, join, isdir
from os import listdir
# TODO: Move the base folder lookup to single method


class Zenlibrary(ZenAPIBase):
    """
    Present an API interface for interaction with the Zenplaylist object.
    """
    def __init__(self, *args, **kwargs):
        super(Zenlibrary, self).__init__(*args, **kwargs)
        self.lib_path = expanduser("~/Music")

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
