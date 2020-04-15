from kivy.event import EventDispatcher
from os import sep, path, listdir
from kivy.logger import Logger
from os.path import exists
from kivy.properties import NumericProperty, ListProperty
from components.filedrop import FileDrop


class Playlist(EventDispatcher):
    """
    Holds the current playlist class.
    """
    current = NumericProperty(0)
    """ The index of the currently playing track in the queue. """

    queue = ListProperty([])
    """
    Contains a list of dictionaries with the following keys:
        * text: Used to display the track in the playlist
        * filename: Full path to the audio file
    """

    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self._load(store)
        self.file_drop = FileDrop(self)

    def _load(self, store):
        """ Initialize and load previous state """
        # See if there is an existing playlist to restore
        if store.exists("Playlist"):
            if "items" in store.get("Playlist"):
                items = store.get("Playlist")["items"]
                k = 1
                while "item" + str(k) in items.keys():
                    if exists(items["item" + str(k)]):
                        self.add_files(items["item" + str(k)])
                    k += 1
            self.current = store.get("Playlist")["current"]
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
        return self.get_info(index=self.current)

    @staticmethod
    def get_text(file_):
        """
        Return the text to display on the playlist given the specified file.
        """
        parts = file_.split(sep)
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
        store.put("Playlist",
                  current=self.current,
                  items=all_items)

    def set_index(self, index):
        """ Set the currently selected track to the one specified by the index
        """
        if index < len(self.queue):
            self.current = index

    def remove_index(self, index):
        """ Remove the specified track from the queue. """
        if index < len(self.queue):
            self.queue.pop(index)

    @staticmethod
    def get_album_art(audio_file):
        """
        Return the full image filename from the folder
        """
        if audio_file:
            folder = audio_file[0: audio_file.rfind(sep)]
            for f_name in reversed(listdir(folder)):
                if f_name[-4:] in [".png", ".bmp", ".jpg", "jpeg"]:
                    return path.join(folder, f_name)
        return "images/zencode.jpg"

    def get_info(self, filename=None, index=None):
        """
        Return a dictionary containing the information on the track """
        try:
            if index is None:
                parts = filename.split(sep)
            else:
                parts = self.queue[index]["filename"].split(sep)
            return {
                "artist": parts[-3],
                "album": parts[-2],
                "track": parts[-1]}
        except IndexError:
            return {
                "artist": "-",
                "album": "-",
                "track": "-"}
