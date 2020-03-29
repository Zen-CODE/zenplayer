from flask import Flask
from webserver.zenswagger import ZenSwagger
from webserver.response import Response


class ZenWebPlayer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    base_url = "/zenplayer/"

    def __init__(self, ctrl):
        super(ZenWebPlayer, self).__init__()

        self.app = Flask(__name__)
        """ The instance of the Flask application. """

        self.api = ZenPlayerAPI(ctrl, self.app)

        self.add_routes()
        ZenSwagger.init_swagger(self.app)

    def add_routes(self):
        """
        Add the desired function to the flask routes
        """
        route = self.base_url
        for meth in ["play_pause", "volume_up", "volume_down", "play_previous",
                     "play_next", "stop", "get_track_info"]:
            self.app.add_url_rule(route + meth, route + meth,
                                  getattr(self.api, meth), methods=['GET'])

    def run(self, *args, **kwargs):
        """
        Run the underlying flask app
        """
        self.app.run(*args, **kwargs)


class ZenPlayerAPI():
    """
    This class houses the interface to teh active Zenplayer
    """
    def __init__(self, ctrl, app):
        super(ZenPlayerAPI, self).__init__()
        self.ctrl = ctrl
        """ Reference to the controller object. """
        self.app = app
        """ Reference to the flask app context. """

    def get_state(self):
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
            "position": ctrl.position
        }

    def play_pause(self):
        """
        Play or pause the currently active player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.play_pause()
        return Response.from_dict({"action": "success"})

    def volume_up(self):
        """
        Turn up the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.volume_up()
        return Response.from_dict({"action": "success"})

    def volume_down(self):
        """
        Turn down the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.volume_down()
        return Response.from_dict({"action": "success"})

    def play_previous(self):
        """
        Play the previous track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.play_previous()
        return Response.from_dict({"action": "success"})

    def play_next(self):
        """
        Play the next track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.play_next()
        return Response.from_dict({"action": "success"})

    def stop(self):
        """
        Stop the currently playing track.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        """
        self.ctrl.stop()
        return Response.from_dict({"action": "success"})

    def get_track_info(self):
        """
        Return the details of the currently playing track
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the state of the current track.
                schema:
                    $ref: '#/definitions/TrackInfo'
        definitions:
            TrackInfo:
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
                        description: The number of this track on the album.
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
                        enum: ["stopped", "paused", "playing", ""]
                    position:
                        description: The position in the currently active track
                                     as presented by a number between 0 and 1.
                        type: number
        """
        return Response.from_dict({})

    def get_track_cover(self):
        """
        Return the image for the currently playing track.
        tags:
            - ZenPlayer
        responses:
            200:
                description: Return the cover image for the currently active
                             track
                schema:
                    $ref: '#/definitions/TrackInfo'

        """
        pass
