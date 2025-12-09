import streamlit as st
from app_pages.zenplayer import show_zenplayer
from app_pages.zenrandom import show_zenrandom
from app_pages.zeninfo import show_zeninfo
from app_pages.sysinfo import show_sysinfo
from app_pages.musiclib import show_musiclib


def init_navigation() -> None:
    """Initialize the naigation sidebar and return the first page."""

    pages = {
        "ZenPlayer": show_zenplayer,
        "Random Album": show_zenrandom,
        "Artist Info": show_zeninfo,
        "System Info": show_sysinfo,
        "Library info": show_musiclib,
    }

    with st.sidebar:
        st.title("⛩️ ZenPlayerLit")
        st.divider()
        page = st.radio("-", list(pages.keys()))
        st.divider()
        cols = st.columns(3)
        cols[1].image("images/favicon.png")

    pages[page]()


if __name__ == "__main__":
    # st.set_page_config(page_title="ZenPlayerLit", page_icon="images/favicon.png")
    st.set_page_config(page_title="ZenPlayerLit", page_icon="images/favicon.png")
    init_navigation()
