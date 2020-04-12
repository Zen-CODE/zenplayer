from threading import Thread
from webserver.zenwebserver import ZenWebServer
from components.paths import rel_to_base
from json import load
from kivy.logger import Logger


class FlaskThread(Thread):
    """
    Start the Flask Application on a background thread to blocking the GUI.
    """
    def __init__(self, ctrl, config):
        super().__init__()
        self.ctrl = ctrl
        self.config = config

    def run(self):
        """ Run the Flask server with the given configuration options """
        try:
            ZenWebServer(self.ctrl).run(**self.config)
        except OSError as e:
            print(f"Unable to start webserver: error {e}")


class WebServer:
    """
    This classes acts as a controller for the flask webserver, starting and
    stopping it on a background thread.
    """
    _thread = None

    @staticmethod
    def _get_config():
        """
        Return a dictionary with our configuration options.
        """
        with open(rel_to_base("config", "webserver.json")) as f:
            return load(f)

    @staticmethod
    def start(ctrl):
        """ Start the ZenPlayer web API backend. """
        config = WebServer._get_config()
        Logger.info("Webserver: Starting web server ")
        thread = FlaskThread(ctrl, config)
        thread.daemon = True
        thread.start()
        WebServer._thread = thread

    @staticmethod
    def stop():
        if WebServer._thread is not None:
            # TODO
            pass
