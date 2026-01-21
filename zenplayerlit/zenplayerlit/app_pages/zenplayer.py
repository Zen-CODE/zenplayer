import streamlit as st
import requests
from zencore import ZENPLAYER_URL
from styler import Styler
from uuid import uuid4
from mutagen.easyid3 import EasyID3
from functools import lru_cache


class ZenPlayer:
    def __init__(self):
        self.data = {}

    @staticmethod
    def _button(name=None):
        if name:
            requests.get(f"{ZENPLAYER_URL}/zenplayer/{name}")

    def show_control_buttons(self):
        """Adds a row of control buttons to the Streamlit app."""
        prev_, stop_, play_pause_, next_, vol_down_, vol_up_, refresh_ = st.columns(
            spec=[1, 1, 2, 1, 1, 1, 1], border=True
        )
        prev_.button(
            "⏮️",
            on_click=self._button,
            args=("play_previous",),
            width="stretch",
        )
        stop_.button(
            "⏹️",
            on_click=self._button,
            args=("stop",),
            width="stretch",
        )
        play_pause_.button(
            "▶️" if self.data.get("state") != "Playing" else "⏸",
            on_click=self._button,
            args=("play_pause",),
            width="stretch",
        )
        next_.button(
            "⏭️",
            on_click=self._button,
            args=("play_next",),
            width="stretch",
        )
        vol_down_.button(
            "🔉",
            on_click=self._button,
            args=("volume_down",),
            width="stretch",
        )
        vol_up_.button(
            "🔊",
            on_click=self._button,
            args=("volume_up",),
            width="stretch",
        )
        refresh_.button(
            "⟳",
            on_click=self._button,
            width="stretch",
        )

    def show_cover_image(self):
        def get_time(time_s):
            return (
                str(int(time_s / 60)).zfill(2)
                + "m "
                + str(int(time_s % 60)).zfill(2)
                + "s"
            )

        data = self.data
        meta = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_track_meta").json()
        st.image(f"{ZENPLAYER_URL}/zenplayer/get_track_cover?random={uuid4()}")
        st.markdown(
            f"**{data['artist']}: {data['album']}** - "
            f"*{data['file_name'].split('/')[-1].split('.')[0]}*"
        )
        st.write(
            f"{meta['sample_rate']}hz, {meta['bitrate']}kbps, {get_time(meta['length'])}"
        )

        st.write()

    def show_progress_bar(self):
        col1, col2 = st.columns([0.1, 0.9])
        col1.write("Position:")
        col2.progress(self.data["position"], text=None, width="stretch")
        col1.write("Volume:")
        col2.progress(self.data["volume"], text=None, width="stretch")

    @staticmethod
    @lru_cache
    def _get_id3_data(file_name: str) -> dict:
        audio = EasyID3(file_name)
        data = {key.title(): value[0] for key, value in audio.items()}
        return data

    def show_id3_tag(self):
        file_name = self.data["file_name"]
        if file_name.split(".")[-1].lower() == "mp3":
            data = self._get_id3_data(file_name)
            st.markdown("**ID3 Tag Data**")
            st.table(data)
        else:
            st.write("No ID3 tag available for non-mp3 files")

    @staticmethod
    def show_playlist():
        data = requests.get(f"{ZENPLAYER_URL}/zenplaylist/get_playlist").json()
        st.subheader("Playlist")
        st.divider()
        for item in data:
            st.write(item["text"])

    @st.fragment(run_every=5)
    def show_fragment(self):
        self.data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()

        col1, col2 = st.columns(2)
        with col1:
            self.show_cover_image()
            self.show_progress_bar()
            self.show_control_buttons()
            self.show_id3_tag()
        with col2:
            self.show_playlist()

    def show(self):
        Styler.add_header("ZenPlayer", "images/zencode.jpg")
        st.divider()
        self.show_fragment()


def show_zenplayer():
    ZenPlayer().show()
