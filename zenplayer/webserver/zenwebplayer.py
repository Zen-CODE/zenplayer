from flask import Flask, render_template
from webserver.zenswagger import ZenSwagger
from os.path import abspath, dirname, join
from webserver.api.zenplayer.zenplayer import Zenplayer
from webserver.api.zenplaylist.zenplaylist import Zenplaylist
from inspect import ismethod


class ZenWebPlayer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    def __init__(self, ctrl):
        super(ZenWebPlayer, self).__init__()
        templates = join(abspath(dirname(__file__)), "templates")
        app = self.app = Flask(__name__, template_folder=templates)
        """ The instance of the Flask application. """

        self.add_routes("zenplayer", Zenplayer(ctrl))
        self.add_routes("zenplaylist", Zenplaylist(ctrl))
        app.add_url_rule("/", "/", self.index, methods=['GET'])
        ZenSwagger.init_swagger(app)

    @staticmethod
    def _get_public_methods(obj):
        """ Return a list of the public methods of the given object. """
        return [method_name for method_name in dir(obj)
                if ismethod(getattr(obj, method_name))
                and method_name[0] != "_"]

    def add_routes(self, base_url, obj):
        """
        Add the exposed functions of the *obj* object to the *base_url* route.
        """
        route = f"/{base_url}/"
        for mth in self._get_public_methods(obj):
            self.app.add_url_rule(route + mth, route + mth,
                                  getattr(obj, mth), methods=['GET'])

    def run(self, *args, **kwargs):
        """
        Run the underlying flask app
        """
        self.app.run(*args, **kwargs)

    @staticmethod
    def index():
        """
        Serve the index as a minimally functional HTML page
        """
        return render_template("index.html")


