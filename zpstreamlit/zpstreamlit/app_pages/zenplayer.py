import streamlit as st
import requests
from zencore import ZENPLAYER, ZENPLAYER_URL


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
        button_width = 80
        prev_, stop_, play_pause_, next_, vol_down_, vol_up_, refresh_ = st.columns(
            spec=[1, 1, 1, 1, 1, 1, 1], border=True
        )
        prev_.button(
            "⏮",
            on_click=ControlButtons._button,
            args=("play_previous",),
            width=button_width,
        )
        stop_.button(
            "⏹", on_click=ControlButtons._button, args=("stop",), width=button_width
        )
        play_pause_.button(
            "⏯",
            on_click=ControlButtons._button,
            args=("play_pause",),
            width=button_width,
        )
        next_.button(
            "⏭",
            on_click=ControlButtons._button,
            args=("play_next",),
            width=button_width,
        )
        vol_down_.button(
            "🔉",
            on_click=ControlButtons._button,
            args=("volume_down",),
            width=button_width,
        )
        vol_up_.button(
            "🔊",
            on_click=ControlButtons._button,
            args=("volume_up",),
            width=button_width,
        )
        refresh_.button("⟳", on_click=ControlButtons._button, width=button_width)


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
        st.image(f"{ZENPLAYER_URL}/zenplayer/get_track_cover", use_container_width=True)
        # zp.write(streamlit_image_coordinates(
        #     f"{ZENPLAYER_URL}/zenplayer/get_track_cover"),
        #     use_column_width="always")
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
        for item in data:
            st.write(item["text"])


def show_zenplayer():
    print("ZenPlayer: Being called...")

    def buid_ui():
        """Refresh the UI components."""
        ZENPLAYER["data"] = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()

        CoverImage.show()
        ProgressBar.show()
        ControlButtons.show()
        Playlist.show()

    buid_ui()

    # while True:
    #     with zp:
    #         sleep(ZENSLEEP)
    #         print("Re-running zenplayer...")
    #         st.rerun()
    # return zp
