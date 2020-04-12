"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'
from kivy.app import App
from components.controller import Controller
from webserver.webserver import WebServer
from kivy.logger import Logger, LOG_LEVELS
from json import load
from components.paths import rel_to_base


class ZenPlayer(App):
    """
    The App initialisation class
    """
    ctrl = None
    ''' Reference to the instantiated Controller class. '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(rel_to_base("config", "zenplayer.json")) as f:
            self._config = load(f)
        self.init_logging()

    def init_logging(self):
        Logger.setLevel(LOG_LEVELS[self._config["log_level"]])

    def on_pause(self):
        """ Enable support for pause """
        return True

    def on_resume(self):
        """ Enable support for resume """
        pass

    def build(self):
        """ Build the app and return the screen manager """
        self.ctrl = Controller(app=self)
        if self._config["enable_webserver"]:
            WebServer.start(self.ctrl)
        else:
            Logger.info("ZenPlayer: Disabling WebServer")
        return self.ctrl.sm

    def on_stop(self):
        """The app is closing. Save the state."""
        pass


ZenPlayer().run()
