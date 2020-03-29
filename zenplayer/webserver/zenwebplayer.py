from flask import Flask, make_response, jsonify
from webserver.zenswagger import ZenSwagger


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

    def get_response(self, data_dict, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        data_dict.update(self.get_state())
        with self.app.app_context():
            resp = make_response(jsonify(data_dict), code)
            resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    def play_pause(self):
        """
        Play or pause the currently active player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: success
        """
        self.ctrl.play_pause()
        return self.get_response({"action": "success"})

    def volume_up(self):
        """
        Turn up the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: success
        """
        self.ctrl.volume_up()
        return self.get_response({"action": "success"})

    def volume_down(self):
        """
        Turn down the volume of the player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success
        """
        self.ctrl.volume_down()
        return self.get_response({"action": "success"})

    def play_previous(self):
        """
        Play the previous track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success
        """
        self.ctrl.play_previous()
        return self.get_response({"action": "success"})

    def play_next(self):
        """
        Play the next track in the playlist.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success
        """
        self.ctrl.play_next()
        return self.get_response({"action": "success"})

    def stop(self):
        """
        Stop the currently playing track.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success
        """
        self.ctrl.stop()
        return self.get_response({"action": "success"})

    def get_track_info(self):
        """
        Return the details of the currently playing track
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success
                schema:
                    $ref: '#/definitions/TrackInfo'
        definitions:
          TrackInfo:
            type: object
            properties:
                volume:
                  type: number
                artist:
                  type: string
                album:
                  type: string
                track:
                  type: integer
                cover:
                  type: string
                time_display:
                  type: string
                state:
                  type: string
                position:
                  type: number
        """
        return self.get_response({})
