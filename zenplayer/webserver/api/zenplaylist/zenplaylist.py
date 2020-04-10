"""
This module houses teh API interface for the ZenPlaylist
"""
from webserver.api.zenapibase import ZenAPIBase
from webserver.response import Response


class Zenplaylist(ZenAPIBase):
    """
    Present an API interface for interaction with the Zenplaylist object.
    """
    def get_current_info(self):
        """
        Return information on the currently active track.
        ---
        tags:
            - ZenPlaylist
        responses:
            200:
                description: Return information on the currently active  track.
                schema:
                    $ref: '#/definitions/PlaylistTrackInfo'
        definitions:
            PlaylistTrackInfo:
                type: object
                properties:
                    artist:
                        description: The name of the tracks artist.
                        type: string
                    album:
                        description: The name of the album the track is from
                        type: string
                    file:
                        description: The full path to the audio file
                        type: string

        """
        data = self.ctrl.playlist.get_current_info()
        return Response.from_dict(data)

    def get_playlist(self):
        """
        Return the current playlist as a list of full paths to the audio file.
        ---
        tags:
            - ZenPlaylist
        responses:
            200:
                description: Return information on the currently active  track.
                schema:
                    $ref: '#/definitions/Playlist'
        definitions:
            Playlist:
                type: array
                items:
                    $ref: '#/definitions/PlaylistItem'
            PlaylistItem:
                type: object
                properties:
                    text:
                        description: The text for the item displayed in the
                                     playlist
                        type: string
                    filename:
                        description: The full path to the audio file
                        type: string
        """
        return Response.from_dict(self.ctrl.playlist.queue)

    def get_current_art(self):
        """
        Return the image for the currently playing track.
        ---
        tags:
            - ZenPlaylist
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
        pl = self.ctrl.playlist
        file_name = pl.get_current_file()
        image = pl.get_album_art(file_name)
        return Response.from_image(image)
