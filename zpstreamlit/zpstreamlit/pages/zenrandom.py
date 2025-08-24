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
