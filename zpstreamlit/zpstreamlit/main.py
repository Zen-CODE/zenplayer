import streamlit as st
from app_pages.zenplayer import get_zenplayer
from app_pages.zenrandom import get_zenrandom
from app_pages.zeninfo import get_zeninfo
from app_pages.sysinfo import get_sysinfo


def init_app() -> None:
    """Initialize our streamlit app."""
    st.set_page_config(page_title="ZenPlayer ST", page_icon="☯️")


def init_navigation() -> None:
    """Initialize the naigation sidebar and return the first page."""

    pages = {
        "ZenPlayer": get_zenplayer,
        "Random Album": get_zenrandom,
        "Artist Info": get_zeninfo,
        "System Info": get_sysinfo,
    }

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(pages.keys()))

    pages[page]()


if __name__ == "__main__":
    init_app()
    init_navigation()
