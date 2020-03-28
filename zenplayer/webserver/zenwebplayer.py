from flask import Flask
from webserver.zenswagger import ZenSwagger


class ZenWebPlayer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    base_url = "/zenplayer/"

    def __init__(self, ctrl):
        super(ZenWebPlayer, self).__init__()
        self.ctrl = ctrl
        """ Reference to the controller object. """

        self.app = Flask(__name__)
        """ The instance of the Flask application. """

        self.add_routes()
        ZenSwagger.init_swagger(self.app)

    def add_routes(self):
        """
        Add the desired function to the flask routes
        """
        route = self.base_url
        # for meth in ["state", "cover", "previous", "next", "play_pause",
        #              "stop", "volume_up", "volume_down"]:
        for meth in ["play_pause", "index"]:
            self.app.add_url_rule(route + meth, route + meth,
                                  getattr(self, meth), methods=['GET'])

    def index(self):
        return "Hello from ZenPlayer"

    def play_pause(self):
        """
        Play or pause the currently active player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success if we have played or paused the current
                             player.
        """
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.ctrl.play_pause())
        # ZenWebController.ctrl.play_pause()
        return "play_pause"

    def run(self, *args, **kwargs):
        """
        Run the underlying flask app
        """
        self.app.run(*args, **kwargs)
