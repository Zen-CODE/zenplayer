from threading import Thread
from webserver.flask_app import app


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
    def start():
        """ Start the ZenPlayer web API backend. """
        thread = FlaskThread()
        thread.daemon = True
        thread.start()
        WebServer._thread = thread

    @staticmethod
    def stop():
        if WebServer._thread is not None:
            # TODO
            pass
