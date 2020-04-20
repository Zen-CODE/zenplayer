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
from components.config import Config


class ZenPlayer(App):
    """
    The App initialisation class
    """
    ctrl = None
    ''' Reference to the instantiated Controller class. '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config = Config.load("zenplayer.json")
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
        self.ctrl = Controller(app=self, config=self._config)
        if self._config["enable_webserver"]:
            WebServer.start(self.ctrl)
        else:
            Logger.info("ZenPlayer: Disabling WebServer")
        return self.ctrl.zenplayer

    def on_stop(self):
        """The app is closing. Save the state."""
        pass


ZenPlayer().run()
