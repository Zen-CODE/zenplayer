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
    @staticmethod
    def get_classes(ctrl):
        """
        Return a list of (name, class) tuples to load.
        """
        with open(rel_to_base("config", "webserver_classes.json")) as f:
            class_list = load(f)

        return [(name, Loader._get_class(name)(ctrl)) for name in class_list]

    @staticmethod
    def _get_class(name):
        """ Return the class definition given the name of the class"""
        mod_name = name.lower()
        mod = import_module(f"webserver.api.{mod_name}.{mod_name}")
        return getattr(mod, name)
