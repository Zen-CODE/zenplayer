import streamlit as st
from app_pages.zenplayer import get_zenplayer
from app_pages.zenrandom import get_zenrandom
from app_pages.zeninfo import get_zeninfo


pages = {
    "ZenPlayer": get_zenplayer,
    "Random Album": get_zenrandom,
    "Artist Info": get_zeninfo,
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", list(pages.keys()))

pages[page]()
