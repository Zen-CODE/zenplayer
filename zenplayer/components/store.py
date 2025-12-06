"""
This module houses a store factory class.
"""

from kivy.storage.jsonstore import JsonStore
from components.config import Config
from os.path import join, exists
from pickle import load, dump


class StoreFactory:
    """
    A helper class for generating and returning the storage class for settings.
    """

    @staticmethod
    def get():
        """
        Build and return an appropriately configured Storage class
        """
        return JsonStore(join(Config.get_config_folder(), "zenplayer_state.json"))

    @staticmethod
    def load_pickle(file_name, default=None):
        """
        Unpickle the Python object from the given file. If it does
        not exist, return the default value.
        """
        pickle_path = join(Config.get_config_folder(), file_name)
        if exists(pickle_path):
            with open(pickle_path, "rb") as f:
                return load(f)
        else:
            return default

    @staticmethod
    def save_pickle(file_name, obj):
        """
        Pickle the Python object to the given file.
        """
        pickle_path = join(Config.get_config_folder(), file_name)
        with open(pickle_path, "wb", encoding="utf-8") as f:
            dump(obj, f)
