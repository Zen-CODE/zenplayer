from threading import Thread
from webserver.flask_app import app
from flasgger import Swagger
from json import loads
from os.path import dirname, join


class FlaskThread(Thread):
    """
    Start the Flask Application on a background thread to blocking the GUI.
    """
    def run(self):
        app.run(debug=True, use_debugger=True, use_reloader=False)


class WebServer:
    """
    This classes acts as a controller for the flask webserver, starting and
    stopping it on a background thread.
    """

    _thread = None

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
                           config=WebServer.get_swagger_config())


    @staticmethod
    def start():
        """ Start the ZenPlayer web API backend. """
        WebServer.init_swagger(app)
        thread = FlaskThread()
        thread.daemon = True
        thread.start()
        WebServer._thread = thread

    @staticmethod
    def stop():
        if WebServer._thread is not None:
            # TODO
            pass
