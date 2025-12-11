import streamlit as st
from library.library import Library
from os import sep
from pydantic import BaseModel, model_validator
from typing import List, Any, Dict
from os import stat as os_stat
from datetime import datetime


class LibraryFile(BaseModel):
    # Required
    artist: str
    album: str
    file_path: str
    file_ext: str

    # Calculated
    file_size: float
    """File size in MB"""

    created: datetime
    accessed: datetime

    @model_validator(mode="before")
    @classmethod
    def add_fields(cls, data: Any) -> Any:
        # Check if the input is a dictionary or map-like
        if isinstance(data, dict):
            stat_info = os_stat(data["file_path"])
            data["created"] = datetime.fromtimestamp(stat_info.st_ctime)
            data["accessed"] = datetime.fromtimestamp(stat_info.st_atime)
            data["file_size"] = stat_info.st_size / (1024 * 1024)

        return data

    def get_display(self) -> Dict:
        return {
            "Artist": self.artist,
            "Album": self.album,
            "File name": self.file_path.split(sep)[-1],
            "File type": self.file_path.split(".")[-1].lower(),
            "Created": self.created.strftime("%Y-%m-%d %H:%M:%S"),
            "Accessed": self.accessed.strftime("%Y-%m-%d %H:%M:%S"),
            "File size": f"{self.file_size:.2f} MB",
        }


MAX = 100


class LibAnalysis:
    def __init__(self):
        self.library = library = Library({})

        self.file_list = file_list = []
        for i, artist in enumerate(library.get_artists()):
            # if i > MAX:
            #     break

            for k, album in enumerate(library.get_albums(artist)):
                album_path = library.get_path(artist, album)
                for j, track in enumerate(library.get_tracks(artist, album)):
                    # file_list.append(sep.join([album_path, track]))

                    file_list.append(
                        LibraryFile(
                            artist=artist,
                            album=album,
                            file_path=sep.join([album_path, track]),
                            file_ext=track.split(".")[-1],
                        )
                    )
                if cover := library.get_cover_path(artist, album):
                    file_list.append(
                        LibraryFile(
                            artist=artist,
                            album=album,
                            file_path=cover,
                            file_ext=cover.split(".")[-1],
                        )
                    )

    def get_metadata(self) -> dict:
        """Return a dictionary of metadata on the library.

        Sample:
        ```json
        {
            "Artists": 100,
            "Albums": 100,
            "Tracks": 100,
            "Covers": 100
        }
        ```
        """
        artists, albums, tracks, covers = 0, 0, 0, 0
        library = self.library
        for artist in library.get_artists():
            artists += 1
            for album in library.get_albums(artist):
                albums += 1
                tracks += len(library.get_tracks(artist, album))
                if "default.png" not in library.get_cover_path(artist, album):
                    covers += 1

        return {
            "Artists": artists,
            "Albums": albums,
            "Tracks": tracks,
            "Covers": covers,
        }

    def get_file_data(self) -> List[LibraryFile]:
        return self.file_list


def show_musiclib():
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.image("images/zencode.jpg", width=128)
    with col1:
        st.markdown("# Zen Library Info")
    st.divider()

    with st.spinner("Loading Library..."):
        analysis = LibAnalysis()

        st.subheader("Library Metadata")
        col1, col2 = st.columns([0.25, 0.75])
        for name, value in analysis.get_metadata().items():
            col1.markdown(f"**{name}**")
            col2.write(value)

        st.subheader("File Statistics")
        data = [lib_file.get_display() for lib_file in analysis.get_file_data()]
        st.dataframe(data)
