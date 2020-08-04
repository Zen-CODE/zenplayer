"""
This module houses the FileSystemExtractor class
"""
from os import listdir
from os.path import isdir, join


class FileSystemExtractor:
    """
    Helper class for extracting tracks and albums covers from
    folders
    """
    music_types = [".ogg", ".mp3", ".wma"]
    art_types = [".jpg", ".jpeg", ".png", ".gif"]

    @staticmethod
    def get_dirs(folder):
        """
        Return a list of sorted sub-folders.

        Args:
            folder (str): The path to the folder to process
        Returns:
            (list): A sorted list of folder in the specified folder.
        """
        return [f for f in sorted(listdir(folder))
                if isdir(join(folder, f))]

    @staticmethod
    def get_media(folder):
        """
        Return a lists of tracks and covers in the given folder.

        Args:
            folder (str): The path to the folder to process
        Returns:
            (list), (list): A sorted list of music tracks and album images
                            respectively.


        """
        tracks, covers, fse = [], [], FileSystemExtractor
        for item in sorted(listdir(folder)):
            if any([item.endswith(e) for e in fse.music_types]):
                tracks.append(item)
            elif any([item.endswith(e) for e in fse.art_types]):
                covers.append(item)

        return tracks, covers
