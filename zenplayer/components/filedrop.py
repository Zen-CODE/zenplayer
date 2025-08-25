"""
The module houses a helper class for handling file and folder dropping.
"""

from kivy.core.window import Window


class FileDrop:
    """
    Convenience class for handling the dragging and dropping of files.
    """

    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist
        Window.bind(on_dropfile=self.on_dropfile)

    def on_dropfile(self, _widget, file_folder):
        """
        Respond to the dropping of files or folders on the window.
        """
        self.playlist.add_files(file_folder.decode())
