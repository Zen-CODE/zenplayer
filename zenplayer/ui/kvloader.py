"""
This module houses the KVLoader class that prevents the loading of KV files
multiple times.
"""

from kivy.lang import Builder


class KVLoader:
    """
    Helper class to prevent the duplicate loading of KV files.
    """

    _loaded = []

    @staticmethod
    def load(file_name):
        """Load commond kv, ensuring not to do it multiple times."""
        if file_name not in KVLoader._loaded:
            Builder.load_file(file_name)
            KVLoader._loaded.append(file_name)
