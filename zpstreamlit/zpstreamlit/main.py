import streamlit as st
from app_pages.zenplayer import show_zenplayer
from app_pages.zenrandom import show_zenrandom
from app_pages.zeninfo import show_zeninfo
from app_pages.sysinfo import show_sysinfo


def init_app() -> None:
    """Initialize our streamlit app."""
    st.set_page_config(page_title="Zen Player Lit", page_icon="images/favicon.png")


def init_navigation() -> None:
    """Initialize the naigation sidebar and return the first page."""

    pages = {
        "ZenPlayer": show_zenplayer,
        "Random Album": show_zenrandom,
        "Artist Info": show_zeninfo,
        "System Info": show_sysinfo,
    }

    st.sidebar.title("⛩️ Navigation")
    page = st.sidebar.radio("->", list(pages.keys()))

    pages[page]()


if __name__ == "__main__":
    init_app()
    init_navigation()
