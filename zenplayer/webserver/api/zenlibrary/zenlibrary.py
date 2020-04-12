"""
This module houses teh API interface for the Zenlibrary
"""
from webserver.api.zenapibase import ZenAPIBase


from flask import request


class ZenLibrary(ZenAPIBase):
    """
    Present an API interface for interaction with the Zenplaylist object.
    """
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
                    id: ArtistList
                    type: array
                    items:
                        string
        """
        contents = self.ctrl.library.get_artists()
        return self.resp_from_data(contents)

    def get_albums(self):
        r"""
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
                description: Return a list of the artist albums
                schema:
                    id: AlbumList
                    type: array
                    items:
                        string
            400:
                description: No album found for artist=\<artist\>
                schema:
                    id: ErrorMessage
                    type: object
                    properties:
                        message:
                            type: string
                            description: The reason the request failed.
        """
        artist = request.args.get("artist")
        if artist:
            contents = self.ctrl.library.get_albums(artist)
            if contents:
                return self.resp_from_data([name for name in sorted(contents)])
        return self.resp_from_data(
            {"message": f"No album found for artist={artist}"}, 400)
