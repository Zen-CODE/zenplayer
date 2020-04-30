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
        Return a list of artists available in this collection.
        ---
        tags:
            - ZenLibrary
        responses:
            200:
                description: Return a list of artists in the current library.
                schema:
                    id: ArtistList
                    type: array
                    items:
                        type: string
                        description: The name of the artist.
        """
        contents = self.ctrl.library.get_artists()
        return self.resp_from_data(contents)

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
              required: true
        responses:
            200:
                description: Return a list of the artist albums
                schema:
                    id: AlbumList
                    type: array
                    items:
                        $ref: '#/definitions/Album'
            400:
                description: No album found for artist "{artist}"
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
            lib = self.ctrl.library
            lst = sorted(self.ctrl.library.get_albums(artist))
            albums = [{"artist": artist,
                       "album": album,
                       "path": lib.get_path(artist, album)} for album in lst]
            if lst:
                return self.resp_from_data(albums)
        return self.resp_from_data(
            {"message": f"No album found for artist={artist}"}, 400)

    def get_random_album(self):
        """
        Return a random album selected from the library.
        ---
        tags:
            - ZenLibrary
        responses:
            200:
                description: Return a random artist and album.
                schema:
                    $ref: '#/definitions/Album'
        definitions:
            Album:
                type: object
                properties:
                    artist:
                        type: string
                        description: The artist name
                    album:
                        type: string
                        description: The album name
                    path:
                        type: string
                        description: The full path to the folder

        """
        lib = self.ctrl.library
        artist, album = lib.get_random_album()
        return self.resp_from_data({
            "artist": artist,
            "album": album,
            "path": lib.get_path(artist, album)
        })

    def get_album_cover(self):
        """
        Return the image for the currently playing track.
        ---
        tags:
            - ZenLibrary
        parameters:
            - name: artist
              in: query
              type: string
              required: true
            - name: album
              in: query
              type: string
              required: true

        responses:
            200:
                description: Return the cover image for the currently active
                             track
                content:
                    image/*:     # Media type
                        schema:
                            type: string
                            format: binary

        """
        artist = request.args.get("artist", "")
        album = request.args.get("album", "")
        if not (album and artist):
            return self.resp_from_data(
                {"message":  "Please specify a valid artist and album"}, 403)
        else:
            cover = self.ctrl.library.get_album_cover(artist, album)
            return self.resp_from_image(cover)
