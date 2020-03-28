from flask import Flask
from os.path import dirname, join
from flasgger import Swagger
from json import loads


app = Flask(__name__)


class ZenSwagger():
    """
    Manager the swagger API documentation backend.
    """
    @staticmethod
    def get_swagger_config():
        return {
            "headers": [],
            "specs": [{
                    "endpoint": 'apispec_1',
                    "route": '/apispec_1.json',
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True}],
            "static_url_path": "/flasgger_static",
            # "static_folder": "static",  # must be set by user
            "swagger_ui": True,
            "specs_route": "/swagger/"
        }

    @staticmethod
    def init_swagger(app):
        """
        Initialize the Swagger UI application and configuration exposing the
        API documentation. Once running, go to http://localhost:5000/swagger/
        """
        with open(join(dirname(__file__), "swagger.template.json"), "rb") as f:
            return Swagger(app, template=loads(f.read()),
                           config=ZenSwagger.get_swagger_config())


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

        ZenSwagger.init_swagger(self.app)
        self.add_routes()

    def add_routes(self):
        """
        Add the desired function to the flask routes
        """
        route = self.base_url
        # for meth in ["state", "cover", "previous", "next", "play_pause",
        #              "stop", "volume_up", "volume_down"]:
        for meth in ["play_pause", "index"]:
            app.add_url_rule(route + meth, "zenplayer/" + meth,
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
