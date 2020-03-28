from flask import Flask, make_response, jsonify
from webserver.zenswagger import ZenSwagger
from kivy.clock import Clock


class ZenWebPlayer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    base_url = "/zenplayer/"

    def __init__(self, ctrl):
        super(ZenWebPlayer, self).__init__()

        self.app = Flask(__name__)
        """ The instance of the Flask application. """

        self.api = ZenPlayerAPI(ctrl)

        self.add_routes()
        ZenSwagger.init_swagger(self.app)

    def add_routes(self):
        """
        Add the desired function to the flask routes
        """
        route = self.base_url
        # for meth in ["state", "cover", "previous", "next", "play_pause",
        #              "stop", "volume_up", "volume_down"]:
        for meth in ["play_pause", "volume_up", "volume_down", "play_previous",
                     "play_next", "stop"]:
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
    def __init__(self, ctrl):
        super(ZenPlayerAPI, self).__init__()
        self.ctrl = ctrl
        """ Reference to the controller object. """

    @staticmethod
    def get_response(data_dict=None, code=200):
        """
        Generate and return the appropriate HTTP response object containing the
        json version of the *data_dict" dictionary.
        """
        if data_dict is None:
            data_dict = {"message": "success"}

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
        Clock.schedule_once(lambda dt: self.ctrl.play_pause())
        return self.get_response({"status": "success"})

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
        Clock.schedule_once(lambda dt: self.ctrl.volume_up())
        return {"status": "success"}

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
        Clock.schedule_once(lambda dt: self.ctrl.volume_down())
        return {"status": "success"}

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
        Clock.schedule_once(lambda dt: self.ctrl.play_previous())
        return {"status": "success"}

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
        Clock.schedule_once(lambda dt: self.ctrl.play_next())
        return {"status": "success"}

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
        Clock.schedule_once(lambda dt: self.ctrl.stop())
        return {"status": "success"}
