from flask import Flask, render_template
from webserver.zenswagger import ZenSwagger
from components.paths import rel_to_base
from webserver.loader import Loader
import logging


class ZenWebServer:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    def __init__(self, ctrl):
        super().__init__()
        templates = rel_to_base("webserver", "templates")
        app = self.app = Flask(
            __name__,
            template_folder=templates,
            static_url_path='/static',
            static_folder=rel_to_base('webserver', 'static'))
        """ The instance of the Flask application. """

        self.class_data = Loader.get_class_data(ctrl)
        for class_datum in self.class_data:
            self.add_routes(class_datum)
        app.add_url_rule("/", "/", self.index, methods=['GET'])
        ZenSwagger.init_swagger(app, self.class_data)
        self.disable_logs()

    def disable_logs(self):
        """ By default, werkzeug logs every call. Stop that."""

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def add_dashboard(self):
        """ Add the flash dashboard monitoring tool. Note that we move the
        import here to avoid the need to install this as a dependency.
        """
        import flask_monitoringdashboard as dashboard  # noqa
        dashboard.config.init_from(file=rel_to_base("config", "dashboard.ini"))
        dashboard.bind(self.app)

    def add_routes(self, class_datum):
        """
        Add the exposed functions of the *obj* object to the *base_url* route.
        """
        route = f"/{class_datum['name'].lower()}/"
        instance = class_datum["instance"]
        for mth in class_datum["methods"]:
            self.app.add_url_rule(route + mth, route + mth,
                                  getattr(instance, mth), methods=['GET'])

    def run(self, *args, **kwargs):
        """
        Run the underlying flask app
        """
        if kwargs.pop("enable_dashboard", False):
            self.add_dashboard()

        self.app.run(*args, **kwargs)

    def index(self):
        """
        Serve the index as a minimally functional HTML page
        """
        return render_template("index.html", class_data=self.class_data)
