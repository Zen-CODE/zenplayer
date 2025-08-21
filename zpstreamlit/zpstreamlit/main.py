import streamlit as st
import requests
import threading
from time import sleep

ZENPLAYER_URL = "http://9.0.0.13:5000"

class ControlButtons:
    """This class houses the control buttons for the media player."""

    @staticmethod
    def _button(name):
        print("Button clicked: ", name)
        requests.get(f"{ZENPLAYER_URL}/zenplayer/{name}")

    @staticmethod
    def show():
        """Adds a row of control buttons to the Streamlit app."""
        prev_, stop_, play_pause_, next_ = st.columns(spec=[1, 1, 1, 1], border=True)
        prev_.button("⏮", on_click=ControlButtons._button, args=("play_previous",), width=150)
        stop_.button("⏹", on_click=ControlButtons._button, args=("stop",), width=150)
        play_pause_.button("⏯", on_click=ControlButtons._button, args=("play_pause",), width=150)
        next_.button("⏭", on_click=ControlButtons._button, args=("play_next",), width=150)


class CoverImage:
    """This class handles the display of the cover image for the media player."""

    @staticmethod
    def show():
        data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
        st.image(f"{ZENPLAYER_URL}/zenplayer/get_track_cover",
                 use_container_width=True)
        st.markdown(f"{data['artist']}: {data['album']} - " \
                         f"{data['file_name'].split('/')[-1].split('.')[0]}")

class ProgressBar:

    @staticmethod
    def show():
       data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
       bar = st.progress(data["position"], text=None, width="stretch")
       while True:
        sleep(1)
        data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
        bar.progress(data["position"], text=None, width="stretch")

st.title("ZenPlayer")
CoverImage.show()
ControlButtons.show()
ProgressBar.show()
