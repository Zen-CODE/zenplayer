import streamlit as st
from app_pages.zenplayer import show_zenplayer
from app_pages.zenrandom import show_zenrandom
from app_pages.zeninfo import show_zeninfo
from app_pages.sysinfo import show_sysinfo
from app_pages.musiclib import show_musiclib


def set_page(name: str, func_name: callable):
    st.session_state.page = name
    func_name()


def init_navigation() -> None:
    """Initialize the naigation sidebar and return the first page."""

    pages = {
        "ZenPlayer": lambda: set_page("zenplayer", show_zenplayer),
        "Random Album": lambda: set_page("random", show_zenrandom),
        "Artist Info": lambda: set_page("zeninfo", show_zeninfo),
        "System Info": lambda: set_page("sysinfo", show_sysinfo),
        "Library info": lambda: set_page("musilib", show_musiclib),
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
    st.set_page_config(
        page_title="ZenPlayerLit", page_icon="images/favicon.png", layout="wide"
    )
    init_navigation()
