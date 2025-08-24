import streamlit as st
from .zencore import ZENPLAYER_URL
import requests
from html import escape


def get_zenrandom():

    random = requests.get(f"{ZENPLAYER_URL}/zenlibrary/get_random_album").json()
    st.markdown(f"**Artist:** {random['artist']}")
    st.markdown(f"**Album:** {random['album']}" )
    url = f"{ZENPLAYER_URL}/zenlibrary/get_album_cover?" \
          f"artist={escape(random['artist'])}&album={escape(random['album'])}"
    st.image(url, use_container_width=True)

    class Buttons:
        @staticmethod
        def click(action=None, artist=None, album=None):
            if action:
                requests.get(f"{ZENPLAYER_URL}/zenplaylist/add_files?" \
                            f"{escape(random['artist'])}/{escape(random['album'])}")
            else:
                st.rerun()

    button_width = 80
    add_, replace_, insert_, next_, next_album_ = st.columns(
        spec=[1, 1, 1, 1, 1], border=True)

    add_.button("Add",
                on_click=Buttons.click, args=("add", random["artist"], random["album"]),
                width=button_width)
    replace_.button("Replace",
                on_click=Buttons.click, args=("replace", random["artist"], random["album"]),
                width=button_width)
    insert_.button("Insert",
                on_click=Buttons.click, args=("insert", random["artist"], random["album"]),
                width=button_width)
    next_.button("Next",
                on_click=Buttons.click, args=("next", random["artist"], random["album"]),
                width=button_width)
    next_album_.button("Another",
                on_click=Buttons.click,
                width=button_width)

