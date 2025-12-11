import streamlit as st
from library.library import Library
from os import sep


MAX = 100


class LibAnalysis:
    def __init__(self):
        self.library = library = Library({})

        self.file_list = file_list = []
        for i, artist in enumerate(library.get_artists()):
            if i > MAX:
                break

            for k, album in enumerate(library.get_albums(artist)):
                album_path = library.get_path(artist, album)
                for j, track in enumerate(library.get_tracks(artist, album)):
                    file_list.append(sep.join([album_path, track]))

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


def show_musiclib():
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.image("images/zencode.jpg", width=128)
    with col1:
        st.markdown("# Zen Library Info")
    st.divider()

    st.subheader("Library Metadata")

    with st.spinner("Loading Library..."):
        analysis = LibAnalysis()

        assert analysis

        col1, col2 = st.columns([0.25, 0.75])
        for name, value in analysis.get_metadata().items():
            col1.markdown(f"**{name}**")
            col2.write(value)

        st.write("Library loaded")
