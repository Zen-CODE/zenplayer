"""This module houses the File Firestore functions - a file-based implementation
of the FireStore backend for ZenPlayer.
"""

from datetime import datetime, timedelta
from socket import gethostname

from components.config import Config
from os.path import exists
from csv import DictWriter
from dataclasses import dataclass
from typing import List

RED = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"  # Essential to stop coloring subsequent output


@dataclass
class StoreEntry:
    artist: str | None = None
    album: str | None = None
    track: str | None = None
    state: str | None = None
    machine: str | None = None
    datetime: str | None = None


class NowPlaying(StoreEntry):
    """This class defines the model mappings to the FileStore csv structure."""

    def __str__(self):
        """Output a pretty format for the console."""
        text = f"{BLUE}NowPlaying - ZenPlayer:{RESET}"
        for field in self.get_fields():
            text += f"\n    {CYAN}{field.capitalize()}:{RESET} {getattr(self, field)}"
        return text

    def get_fields(self) -> List[str]:
        """Return a list of field / columns names we store."""
        return list(self.__dataclass_fields__.keys())

    def save(self):
        """Save the item to the csv file."""
        csv_file = Config.get_config_folder() + "/nowplaying.csv"

        mode = "a" if exists(csv_file) else "w"
        with open(csv_file, mode, newline="") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.get_fields())
            if mode == "w":
                writer.writeheader()
            prop_dict = {f: getattr(self, f) for f in self.get_fields()}
            writer.writerow(prop_dict)

    def write_to_db(self, ctrl):
        """Write the given values from the controller to our csv file."""
        np = NowPlaying(
            artist=ctrl.artist,
            album=ctrl.album,
            track=ctrl.track,
            state=ctrl.state,
            machine=gethostname(),
            datetime=datetime.now() - timedelta(hours=2),
        )
        print(str(np))
        np.save()
