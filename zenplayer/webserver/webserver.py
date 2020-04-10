from threading import Thread
from webserver.zenwebplayer import ZenWebPlayer


class FlaskThread(Thread):
    """
    Start the Flask Application on a background thread to blocking the GUI.
    """
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl

    def run(self):
        try:
            ZenWebPlayer(self.ctrl).run(
                debug=True, use_debugger=True, use_reloader=False,
                host="0.0.0.0")
        except OSError as e:
            print(f"Unable to start webserver: error {e}")


class WebServer:
    """
    This classes acts as a controller for the flask webserver, starting and
    stopping it on a background thread.
    """
    _thread = None

    @staticmethod
    def start(ctrl):
        """ Start the ZenPlayer web API backend. """
        thread = FlaskThread(ctrl)
        thread.daemon = True
        thread.start()
        WebServer._thread = thread

    @staticmethod
    def stop():
        if WebServer._thread is not None:
            # TODO
            pass
