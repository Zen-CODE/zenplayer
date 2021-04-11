"""
This module houses a helper class for loading configuration files.
"""
from kivy.logger import Logger
from os.path import expanduser, exists, join
from os import makedirs
from components.paths import rel_to_base
from kivy.utils import platform
from shutil import copy
from json import load


class Config:
    """
    Helper class for loading confgiguration file from the user folder and
    establishing sensible defaults
    """
    @staticmethod
    def _get_default(file_name):
        """ Returns the full path for the OS specified default for conig file
        """
        config = rel_to_base("config", file_name.replace(".", f".{platform}."))
        if exists(config):
            return config
        return rel_to_base("config", file_name)

    @staticmethod
    def get_config_folder():
        """ Return the path to the config folder """
        path = expanduser("~/.zencode/zenplayer")
        if not exists(path):
            makedirs(path)
        return path

    @staticmethod
    def load(file_name):
        """
        Load the configuration from the specified file file. This is loaded
        from the user home folder. If none exists, one is copied there.
        """

        cfg_path = join(Config.get_config_folder(), file_name)
        if not exists(cfg_path):
            copy(Config._get_default(file_name), cfg_path)
        Logger.info("Config: Loading config from %s", cfg_path)
        with open(cfg_path) as f:
            return load(f)
