"""
Houses a convenience function for obtaining absolute file paths relative to the
ZenPlayer root folder.
"""
from os.path import abspath, dirname, join, sep

_base = abspath(dirname(abspath(__file__)) + sep + ".." + sep)


def rel_to_base(*paths):
    """
    Return the full path of the *paths relative to the ZenPlayer root folder.
    """
    return join(_base, *paths)
