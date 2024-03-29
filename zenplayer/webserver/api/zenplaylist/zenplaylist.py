"""
This module houses the API interface for the ZenPlaylist object.
"""
from webserver.api.zenapibase import ZenAPIBase
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
                    track_name:
                        description: The name of the track
                        type: string
                    track_number:
                        description: The number of the track on the album
                        type: integer

        """
        data = self.ctrl.playlist.get_current_info()
        return self.resp_from_data(data)

    def get_playlist(self):
        """
        Return the current playlist as a sequenctial list of items
        ---
        tags:
            - ZenPlaylist
        responses:
            200:
                description: Return the tracks in the current playlist.
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

    def get_playlist_meta(self):
        """
        Return the current playlist enhanced with metadata.
        ---
        tags:
            - ZenPlaylist
        responses:
            200:
                description: Return the tracks in the current playlist.
                schema:
                    $ref: '#/definitions/PlaylistMeta'
        definitions:
            PlaylistMeta:
                type: array
                items:
                    $ref: '#/definitions/PlaylistMetaItem'
            PlaylistMetaItem:
                type: object
                properties:
                    active:
                        description: Indicates whether this track is currently
                                     playing.
                        type: boolean
                    text:
                        description: The text for the item displayed in the
                                     playlist
                        type: string
                    artist:
                        description: The name of the artist of this track
                        type: string
                    album:
                        description: The name of the album this track is on.
                        type: string
                    track_name:
                        description: The name of the track.
                        type: string
                    track_number:
                        description: The number of the track.
                        type: string
                    album:
                        description: The name of the album this track is on.
                        type: string
                    filename:
                        description: The full path to the audio file
                        type: string
        """
        pl = self.ctrl.playlist
        ret, active = pl.queue[:], pl.get_current_info()
        for item in ret:
            item.update(pl.get_info(item["filename"]))
            item["active"] = bool(active["track"] == item["track"])
        return self.resp_from_data(ret)

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
            - name: mode
              description: Specifies the way in which the files should be
                           added.
              in: query
              type: string
              enum: ["add", "replace", "insert", "next", "next_album"]
              required: false

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
                description: The folder could not be found.
        """
        folder = self.get_request_arg("folder")
        if folder or not exists(folder):
            mode = self.get_request_arg("mode", "add")
            response = self.safe_call(
                self.ctrl.playlist.add_files, folder, mode)
            if mode in ["replace", "insert"]:
                self.safe_call(self.ctrl.play_index, 0, get_response=False)
            return response

        else:
            return self.resp_from_data(
                {"message": f"No such folder found: '{folder}'"}, 404)
