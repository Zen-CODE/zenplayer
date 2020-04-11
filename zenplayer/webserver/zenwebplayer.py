from flask import Flask, render_template
from webserver.zenswagger import ZenSwagger
from inspect import ismethod
from components.paths import rel_to_base
from webserver.loader import Loader


class ZenWebPlayer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    def __init__(self, ctrl):
        super().__init__()
        templates = rel_to_base("webserver", "templates")
        app = self.app = Flask(__name__, template_folder=templates)
        """ The instance of the Flask application. """

        classes = Loader().get_classes(ctrl)
        for name, instance in classes:
            self.add_routes(name.lower(), instance)
        app.add_url_rule("/", "/", self.index, methods=['GET'])
        ZenSwagger.init_swagger(app, classes)

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


