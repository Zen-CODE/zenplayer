"""This module houses the File Firestore functions - a file-based implementation
of the FireStore backend for ZenPlayer.
"""

from datetime import datetime, timedelta
from socket import gethostname

from components.config import Config
from kivy.logger import Logger
from os.path import exists
from csv import DictWriter, DictReader
from dataclasses import dataclass
from typing import List


@dataclass
class StoreEntry:
    artist: str | None = None
    album: str | None = None
    track: str | None = None
    state: str | None = None
    machine: str | None = None
    datetime: str | None = None


class NowPlaying(StoreEntry):
    """This class defines the model mappings to the FileStore csv structure.

    Note: When instantiating this class, the constructor keyword arguments
          must contain at least the following keys:


    """

    _csv_file = Config.get_config_folder() + "/nowplaying.csv"

    def get_fields(self) -> List[str]:
        """Return a list of field / columns names we store."""
        return list(self.__dataclass_fields__.keys())

    def save(self):
        """Save the item to Firestore."""
        mode = "a" if exists(self._csv_file) else "w"
        with open(self._csv_file, mode, newline="") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.get_fields())
            if mode == "w":
                writer.writeheader()
            prop_dict = {f: getattr(self, f) for f in self.get_fields()}
            writer.writerow(prop_dict)

    def get_last(self) -> dict:
        """Return the last played item."""
        if not exists(NowPlaying._csv_file):
            return {}

        with open(NowPlaying._csv_file, "w", newline="") as csvfile:
            reader = DictReader(csvfile, fieldnames=self.get_fields())
            for line in reader:
                last_row = line
        return last_row

    def write_to_db(self, ctrl):
        """Write the given values to our csv file."""
        Logger.info("NowPlaying: Adding entry to the csv file...")
        np = NowPlaying(
            artist=ctrl.artist,
            album=ctrl.album,
            track=ctrl.track,
            state=ctrl.state,
            machine=gethostname(),
            datetime=datetime.now() - timedelta(hours=2),
        )
        np.save()
