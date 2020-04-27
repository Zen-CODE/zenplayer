"""
This module houses teh API interface for the Zenplaylist
"""
from webserver.api.zenapibase import ZenAPIBase
from flask import request
from os.path import exists


class ZenPlaylist(ZenAPIBase):
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
                    track:
                        description: The name of the track (audio file name)
                        type: string

        """
        data = self.ctrl.playlist.get_current_info()
        return self.resp_from_data(data)

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
        return self.resp_from_data(self.ctrl.playlist.queue)

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
        return self.resp_from_image(image)

    def add_files(self):
        """
        Add the specified folder or file to the playlist
        ---
        tags:
            - ZenPlaylist
        parameters:
            - name: folder
              in: query
              type: string
              required: true

        responses:
            200:
                description: The folder was successfully added to the playlist.
                schema:
                    id:
                    type: object
                    properties:
                        message:
                            description: Contains a description of the
                                         response.
                            type: string
            404:
                description: THe folder would not befounf
        """
        folder = request.args.get("folder")
        if folder or not exists(folder):
            self.ctrl.playlist.add_files(folder)
            return self.resp_from_data(
                {"message": f"Folder '{folder}' added to playlist"})

        else:
            return self.resp_from_data(
                {"message": f"No such folder found: '{folder}'"}, 404)
