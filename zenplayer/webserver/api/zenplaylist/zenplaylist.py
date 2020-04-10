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

