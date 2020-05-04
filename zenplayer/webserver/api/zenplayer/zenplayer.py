from components.meta import Metadata
from kivy.clock import Clock
from webserver.api.zenapibase import ZenAPIBase
from flask import request


class ZenPlayer(ZenAPIBase):
    """
    This class houses the interface to the active ZenPlayer Kivy application.
    """

    def _get_state(self):
        """
        Return a dictionary containing the complete player state.
        """
        ctrl = self.ctrl
        return {
            "volume": ctrl.volume,
            "artist": ctrl.artist,
            "album": ctrl.album,
            "track": ctrl.track,
            "cover": ctrl.cover,
            "time_display": ctrl.time_display,
            "state": ctrl.state,
            "position": ctrl.position,
            "file_name": ctrl.file_name
        }

    def get_track_meta(self):
        """
        Return the technical metadata on the current track
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackMeta'
        definitions:
            TrackMeta:
                type: object
                properties:
                    length:
                        description: The length of the track in seconds.
                        type: number
                    bitrate:
                        description: The bitrate in kbps
                        type: integer
                    channels:
                        description: The number of audio channels
                        type: integer
                    sample_rate:
                        description: The audio sample rate in Hz.
                        type: integer

        """
        meta = Metadata.get(self.ctrl.file_name)
        return self.resp_from_data(meta)

    def play_pause(self):
        """
        Play or pause the currently active player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        definitions:
            ActionResponse:
                type: object
                properties:
                    status:
                        description: Indicates whether the action was
                                     successful or not.
                        type: string
                        enum: ["success", "failed"]

        """
        return self.safe_call(self.ctrl.play_pause)

    def volume_set(self):
        """
        Set the volume of the player to a specific value.
        ---
        tags:
            - ZenPlayer
        parameters:
            - name: volume
              in: query
              type: string
              required: true

        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        def get_float(value):
            try:
                return float(value)
            except Exception:
                return None

        val = get_float(request.args.get("volume", None))
        if val is not None:
            return self.safe_call(self.ctrl.on_volume, None, val)
        else:
            return self.resp_from_data(
                {"message": "Invalid value for volume"}, 400)

    def volume_up(self):
        """
        Turn up the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        return self.safe_call(self.ctrl.volume_up)

    def volume_down(self):
        """
        Turn down the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        return self.safe_call(self.ctrl.volume_down)

    def play_previous(self):
        """
        Play the previous track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        return self.safe_call(self.ctrl.play_previous)

    def play_next(self):
        """
        Play the next track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        return self.safe_call(self.ctrl.play_next)

    def stop(self):
        """
        Stop the currently playing track.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the status of the requested action.
                schema:
                    $ref: '#/definitions/ActionResponse'
        """
        return self.safe_call(self.ctrl.stop)

    def get_state(self):
        """
        Return the state of the ZenPlayer. This include details of the
        currently playing track.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/PlayingTrackInfo'
        definitions:
            PlayingTrackInfo:
                type: object
                properties:
                    volume:
                        description: The current volume between 0 and 1.
                        type: number
                    artist:
                        description: The artist of the currently active track.
                        type: string
                    album:
                        description: The album the currently active track is
                                     from.
                        type: string
                    track:
                        description: The file name of the currently playing
                                     track.
                        type: integer
                    cover:
                        description: The full local path to the cover for the
                                     currently active track.
                        type: string
                    time_display:
                        description: The current position in the track
                                     followed by it's length.
                        type: string
                    state:
                        description: The state of the currently playing track.
                        type: string
                        enum: ["Stopped", "paused", "Playing", ""]
                    position:
                        description: The position in the currently active track
                                     as presented by a number between 0 and 1.
                        type: number
                    file_name:
                        description: The full path of the currently playing
                                     file.
                        type: string
        """
        return self.resp_from_data(self._get_state())

    def get_track_cover(self):
        """
        Return the image for the currently playing track.
        ---
        tags:
            - ZenPlayer
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
        state = self._get_state()
        return self.resp_from_image(state["cover"])
