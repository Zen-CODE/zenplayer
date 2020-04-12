"""
This module houses a factory class for generating and retuning screens
"""
from ui.screens.playlist.playlist import PlaylistScreen
from importlib import import_module


class ScreenFactory:
    """
    A convenience class for generating and returning screens for use in
    ZenPlayer
    """
    @staticmethod
    def get(name, **kwargs):
        """
        Create and return a screen of the type specified by *name* and pass it
        the given **kwargs**.
        """
        # e.g. ui.screens.playlist.playlist.PlaylistScreen
        mod = import_module(f"ui.screens.{name.lower()}.{name.lower()}")
        return getattr(mod, f"{name}Screen")(name=name, **kwargs)
