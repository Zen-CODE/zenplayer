"""
This module houses a store factory class.
"""
from kivy.storage.jsonstore import JsonStore
from os.path import join, expanduser, exists
from os import mkdir


class StoreFactory:
    """
    A helper class for generating and returning the storage class for settings.
    """
    @staticmethod
    def get():
        """
        Build and return an appropriately configured Storage class
        """
        return JsonStore(join(StoreFactory._get_settings_folder(),
                              "zenplayer.json"))

    @staticmethod
    def _get_settings_folder():
        """ Return the folder when the setting file is stored. """
        path = expanduser("~/.zencode")
        if not exists(path):
            mkdir(path)
        return path

