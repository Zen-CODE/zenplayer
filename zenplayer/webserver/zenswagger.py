from flasgger import Swagger
from json import loads
from os.path import dirname, join


class ZenSwagger():
    """
    Manager the swagger API documentation backend.
    """
    @staticmethod
    def get_swagger_config():
        return {
            "headers": [],
            "specs": [{
                    "endpoint": 'apispec_v1',
                    "route": '/apispec_v1.json',
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
            return Swagger(app,
                           template=loads(f.read()),
                           config=ZenSwagger.get_swagger_config())
