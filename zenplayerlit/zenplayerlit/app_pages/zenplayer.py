import streamlit as st
import requests
from zencore import ZENPLAYER, ZENPLAYER_URL
from styler import Styler


class ControlButtons:
    """This class houses the control buttons for the media player."""

    @staticmethod
    def _button(name=None):
        print("Button clicked: ", name)
        if name:
            requests.get(f"{ZENPLAYER_URL}/zenplayer/{name}")

    @staticmethod
    def show():
        """Adds a row of control buttons to the Streamlit app."""
        prev_, stop_, play_pause_, next_, vol_down_, vol_up_, refresh_ = st.columns(
            spec=[1, 1, 2, 1, 1, 1, 1], border=True
        )
        prev_.button(
            "⏮️",
            on_click=ControlButtons._button,
            args=("play_previous",),
            width="stretch",
        )
        stop_.button(
            "⏹️",
            on_click=ControlButtons._button,
            args=("stop",),
            width="stretch",
        )
        play_pause_.button(
            "▶️⏸️",
            on_click=ControlButtons._button,
            args=("play_pause",),
            width="stretch",
        )
        next_.button(
            "⏭️",
            on_click=ControlButtons._button,
            args=("play_next",),
            width="stretch",
        )
        vol_down_.button(
            "🔉",
            on_click=ControlButtons._button,
            args=("volume_down",),
            width="stretch",
        )
        vol_up_.button(
            "🔊",
            on_click=ControlButtons._button,
            args=("volume_up",),
            width="stretch",
        )
        refresh_.button(
            "⟳",
            on_click=ControlButtons._button,
            width="stretch",
        )


class CoverImage:
    """This class handles the display of the cover image for the media player."""

    @staticmethod
    def show():
        def get_time(time_s):
            return (
                str(int(time_s / 60)).zfill(2)
                + "m "
                + str(int(time_s % 60)).zfill(2)
                + "s"
            )

        data = ZENPLAYER["data"]
        meta = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_track_meta").json()
        st.image(f"{ZENPLAYER_URL}/zenplayer/get_track_cover")
        st.markdown(
            f"**{data['artist']}: {data['album']}** - "
            f"*{data['file_name'].split('/')[-1].split('.')[0]}*"
        )
        st.write(
            f"{meta['sample_rate']}hz, {meta['bitrate']}kbps, {get_time(meta['length'])}"
        )

        st.write()


class ProgressBar:
    @staticmethod
    def show():
        st.progress(ZENPLAYER["data"]["position"], text=None, width="stretch")


class Playlist:
    @staticmethod
    def show():
        Playlist.update()

    @staticmethod
    def update():
        data = requests.get(f"{ZENPLAYER_URL}/zenplaylist/get_playlist").json()
        st.subheader("Playlist")
        st.divider()
        for item in data:
            st.write(item["text"])


class ZenPlayer:
    @staticmethod
    def show():
        Styler.add_header("ZenPlayer", "images/zencode.jpg")
        ControlButtons.show()
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            CoverImage.show()
            ProgressBar.show()
        with col2:
            Playlist.show()


@st.fragment(run_every=5)
def show_zenplayer():
    ZENPLAYER["data"] = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
    ZenPlayer.sh
