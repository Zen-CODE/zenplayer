"""
This module provides a help class to dynamically loads and present classes and
modules for both swagger docs and the zenwebserver.
"""
from components.paths import rel_to_base
from json import load
from importlib import import_module


class Loader:
    """
    A convenience class for dynamically loading webserver modules.
    """
    def __init__(self):
        super().__init__()
        with open(rel_to_base("config", "webserver_classes.json")) as f:
            self._config = load(f)

    def get_classes(self, ctrl):
        """
        Return a list of (name, class) tuples to load.
        """
        ret = []
        for item in self._config:
            name = item["name"].lower()
            mod = import_module(f"webserver.api.{name}.{name}")
            ret.append((item["name"], getattr(mod, item["name"])(ctrl)))
        return ret
