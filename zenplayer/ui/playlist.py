"""
This class houses the PlayList class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty, NumericProperty, BooleanProperty,
                             ListProperty)
from os import sep, path, listdir
from kivy.logger import Logger
from os.path import exists
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.event import EventDispatcher


class PlayList(object):
    """
    Holds the current playlist class.
    """
    current = 0
    """ The index of the currently playing track in the queue. """

    queue = []
    """
    Contains a list of dictionaries with the following keys:
        * text: Used to display the track in the playlist
        * filename: Full path to the audio file
    """

    def __init__(self, store):

        super(PlayList, self).__init__()
        self._load(store)

    def _load(self, store):
        """ Initialize and load previous state """
        # See if there is an existing playlist to restore
        if store.exists("playlist"):
            if "items" in store.get("playlist"):
                items = store.get("playlist")["items"]
                k = 1
                while "item" + str(k) in items.keys():
                    if exists(items["item" + str(k)]):
                        self.add_files(items["item" + str(k)])
                    k += 1
            self.current = store.get("playlist")["current"]
            if self.current >= len(self.queue) - 1:
                self.current = 0

    def get_current_file(self):
        """Returns the filename of the current audio file."""
        if len(self.queue) > self.current:
            return self.queue[self.current]["filename"]
        else:
            return ""

    def get_current_info(self):
        """ Return a dictionary of information on the current track"""
        if len(self.queue) > self.current:
            return self.get_info(self.queue[self.current]["filename"])
        else:
            return {}

    @staticmethod
    def get_text(file_folder):
        """
        Return the text to display on the playlist given the specified file.
        """
        parts = file_folder.split(sep)
        return " - ".join(parts[-3:])

    def add_files(self, file_folder):
        """ Add the specified folder to the queue """
        Logger.info("playlist.py: processing {0}".format(file_folder))
        if path.isdir(file_folder):
            for f in sorted(listdir(file_folder)):
                self.add_files(path.join(file_folder, f))
        elif file_folder[-3:] in ["mp3", "ogg", "wav", "m4a"]:
            self.queue.append({"filename": file_folder,
                               "text": self.get_text(file_folder)})

    def clear_files(self):
        """ Clear the existing playlist"""
        self.queue = []
        self.current = 0

    def move_next(self):
        """ Move the selected track to the next"""
        if len(self.queue) > self.current:
            self.current += 1
        elif len(self.queue) > 0:
            self.current = 1
        else:
            self.current = 0

    def move_previous(self):
        """ Move the selected track to the previous entry"""
        if 0 < self.current:
            self.current += -1

    def remove_current(self):
        """ Remove the currently playing track from the playlist """
        if self.current < len(self.queue):
            self.queue.pop(self.current)

    def save(self, store):
        """ The playlist screen is being closed """
        all_items = {}
        for k, item in enumerate(self.queue):
            all_items.update({"item" + str(k + 1): item["filename"]})
        store.put("playlist",
                  current=self.current,
                  items=all_items)

    def set_index(self, index):
        """ Set the currently selected track to the one specified by the index
        """
        if index < len(self.queue):
            self.current = index

    @staticmethod
    def get_albumart(audiofile):
        """
        Return the full image filename from the folder
        """
        folder = audiofile[0: audiofile.rfind(sep)]
        for f_name in reversed(listdir(folder)):
            if f_name[-4:] in [".png", ".bmp", ".jpg", "jpeg"]:
                return path.join(folder, f_name)
        return "images/zencode.jpg"

    @staticmethod
    def get_info(filename):
        """
        Return a dictionary containing the metadata on the track """
        try:
            parts = filename.split(sep)
            return {
                "artist": parts[-3],
                "album": parts[-2],
                "file": parts[-1]}
        except IndexError:
            return {
                "artist": "-",
                "album": "-",
                "file": "-"}


class PlayListScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """

    def __init__(self, sm, ctrl, playlist, **kwargs):
        Builder.load_file("ui/playlist.kv")
        self.sm = sm
        self.playlist = playlist
        self.ctrl = ctrl
        super(PlayListScreen, self).__init__(**kwargs)

        self.ids.rv.data = self.playlist.queue
