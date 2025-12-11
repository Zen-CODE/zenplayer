import streamlit as st
from library.library import Library
from os import sep


MAX = 100


class LibAnalysis:
    def __init__(self):
        library = Library({})

        self.file_list = file_list = []
        for i, artist in enumerate(library.get_artists()):
            if i > MAX:
                break

            for k, album in enumerate(library.get_albums(artist)):
                album_path = library.get_path(artist, album)
                for j, track in enumerate(library.get_tracks(artist, album)):
                    file_list.append(sep.join([album_path, track]))


def show_musiclib():
    with st.spinner("Loading Library..."):
        analysis = LibAnalysis()

        assert analysis
        st.write("Library loaded")
