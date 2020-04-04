"""
This module houses a factory class for generating and retuning screens
"""
from ui.screens.playlist.playlist import PlaylistScreen
from ui.screens.filebrowser.filebrowser import ZenFileBrowser


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
        return getattr(ScreenFactory, f"_get_{name}")(name=name, **kwargs)

    @staticmethod
    def _get_playlist(**kwargs):
        """ Return the PlaylistScreen """
        return PlaylistScreen(**kwargs)

    @staticmethod
    def _get_filebrowser(**kwargs):
        """ Return the PlaylistScreen """
        return ZenFileBrowser(**kwargs)
