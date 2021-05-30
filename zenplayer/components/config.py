"""This module houses a helper class for loading configuration files."""
from json import load
from os.path import exists, expanduser, join
from os import makedirs
from shutil import copy


from kivy.logger import Logger
from kivy.utils import platform

from components.paths import rel_to_base


class Config:
    """Helper class for loading configuration files with sensible defaults."""

    @staticmethod
    def _get_default(file_name):
        """Return the full path for the OS specified default config file."""
        config = rel_to_base("config", file_name.replace(".", f".{platform}."))
        if exists(config):
            return config
        return rel_to_base("config", file_name)

    @staticmethod
    def get_config_folder():
        """Return the path to the config folder."""
        path = expanduser("~/.zencode/zenplayer")
        if not exists(path):
            makedirs(path)
        return path

    @staticmethod
    def load(file_name):
        """Load the configuration from the specified file_name.

        This is loaded from the user home folder. If it does not exists, one is
        copied there as a template.
        """
        cfg_path = join(Config.get_config_folder(), file_name)
        if not exists(cfg_path):
            copy(Config._get_default(file_name), cfg_path)
        Logger.info("Config: Loading config from %s", cfg_path)
        with open(cfg_path) as f:
            return load(f)
