"""
This module houses the logging setup and configuration
"""
from logging.config import dictConfig
from json import load
from os.path import dirname, abspath, join


def init_logging():
    """ Setup the logging configuration """
    cfg_path = join(dirname(abspath(__file__)), "../config/logging.json")
    with open(cfg_path, 'rt') as f:
        config = load(f)
        dictConfig(config)
