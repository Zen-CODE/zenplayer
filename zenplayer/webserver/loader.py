"""
This module provides a help class to dynamically loads and present classes and
modules for both swagger docs and the zenwebserver.
"""

from components.config import Config
from importlib import import_module
from inspect import ismethod


class Loader:
    """
    A convenience class for dynamically loading webserver modules.
    """

    @staticmethod
    def get_class_data(ctrl):
        """
        Return a list of dictionaries, where each dictionary contains the
        following keys:

            "name": The name of the class
            "instance": A reference to the instantiated instance of this class
            "methods": A list of public methods of the class exposed for the
                       API
        """
        class_list = Config.load("webserver_classes.json")
        ret = []
        for name in class_list:
            obj = Loader._get_class(name)(ctrl)
            ret.append(
                {
                    "name": name,
                    "instance": obj,
                    "methods": Loader._get_public_methods(obj),
                }
            )
        return ret

    @staticmethod
    def _get_class(name):
        """Return the class definition given the name of the class"""
        mod_name = name.lower()
        mod = import_module(f"webserver.api.{mod_name}.{mod_name}")
        return getattr(mod, name)

    @staticmethod
    def _get_public_methods(obj):
        """Return a list of the public methods of the given object."""
        return [
            method_name
            for method_name in dir(obj)
            if ismethod(getattr(obj, method_name)) and method_name[0] != "_"
        ]
