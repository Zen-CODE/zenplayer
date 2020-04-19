"""
This module houses a store factory class.
"""
from kivy.storage.jsonstore import JsonStore
from components.config import Config
from os.path import join


class StoreFactory:
    """
    A helper class for generating and returning the storage class for settings.
    """
    @staticmethod
    def get():
        """
        Build and return an appropriately configured Storage class
        """
        return JsonStore(join(Config.get_config_folder(),
                              "zenplayer_state.json"))
