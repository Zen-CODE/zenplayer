"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from os.path import exists
from kivy.lang import Builder
from os.path import sep


class ZenFileBrowser(Screen):
    """
    Displays a file browsing screen for ZenPlayer
    """
    filechooser = ObjectProperty()

    ctrl = ObjectProperty()

    def __init__(self, **kwargs):
        Builder.load_file('ui/screens/filebrowser/filebrowser.kv')
        super().__init__(**kwargs)
        self._init(self.ctrl.store)
        # Hack to make the ScrollView easier to do large scrolls on OSX
        sv = self.filechooser.layout.children[0].children[0]
        sv.bar_width = 15
        sv.scroll_type = ['bars', 'content']

    def _init(self, store):
        """
        The filebrowser screen is being opened for the first time.
        Initialize the paths to the one stored.
        """
        if store.exists("filebrowser"):
            if "path" in store.get("filebrowser").keys():
                file_path = store.get("filebrowser")["path"]
                if exists(file_path):
                    self.filechooser.path = file_path

    def add_replace(self):
        """ Add any selected files/folders to the playlist removing any that
        already exist """
        if self.filechooser.selection:
            self.ctrl.stop()
            self.ctrl.playlist.clear_files()
            for file_folder in self.filechooser.selection:
                self.ctrl.playlist.add_files(file_folder)
            self.ctrl.play_index(0)

    def add_files(self):
        """ Add any selected files/folders to the playlist  """
        if self.filechooser.selection:
            for file_folder in self.filechooser.selection:
                self.ctrl.playlist.add_files(file_folder)

    def folder_up(self):
        """ Move a single folder up """
        path = self.filechooser.path
        if path.rfind(sep) > 1:
            self.filechooser.path = path[:path.rfind(sep)]

    def save(self, store):
        """ Save the file browser state """
        if len(self.filechooser.selection) > 0:
            store.put("filebrowser", path=self.filechooser.selection[0])
