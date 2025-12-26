import streamlit as st
from zencore import ZENPLAYER_URL
import requests
from html import escape
from styler import Styler
from functools import partial
from urllib.parse import quote


def show_zenrandom():
    if term := st.session_state.get("search"):
        random = requests.get(f"{ZENPLAYER_URL}/zenlibrary/search?query={term}").json()
    else:
        random = requests.get(f"{ZENPLAYER_URL}/zenlibrary/get_random_album").json()

    Styler.add_header("Random album", "images/zencode.jpg")
    st.divider()

    if random:

        class Buttons:
            @staticmethod
            def click(action=None, artist=None, album=None):
                if action and "path" in random.keys():
                    response = requests.get(
                        f"{ZENPLAYER_URL}/zenplaylist/add_files?folder="
                        f"{escape(random['path'])}&mode={action}"
                    )
                    if 200 <= response.status_code <= 204:
                        st.info(f"{random['path']} added to playlist ({action})..")
                    else:
                        st.error("Error adding to playlist!")

        add_, replace_, insert_, next_, next_album_ = st.columns(
            spec=[1, 1, 1, 1, 1], border=True
        )

        add_.button(
            "Add",
            on_click=partial(Buttons.click, "add", random["artist"], random["album"]),
            width="stretch",
        )
        replace_.button(
            "Replace",
            on_click=partial(
                Buttons.click, "replace", random["artist"], random["album"]
            ),
            width="stretch",
        )
        insert_.button(
            "Insert",
            on_click=partial(
                Buttons.click, "insert", random["artist"], random["album"]
            ),
            width="stretch",
        )
        next_.button(
            "Next",
            on_click=partial(Buttons.click, "next", random["artist"], random["album"]),
            width="stretch",
        )
        next_album_.button(
            "Another",
            on_click=lambda: None,
            width="stretch",
        )

        Styler.add_row("Artist", random["artist"])
        Styler.add_row("Album", random["album"])

        url = (
            f"{ZENPLAYER_URL}/zenlibrary/get_album_cover?"
            f"artist={quote(random['artist'])}&album={quote(random['album'])}"
        )
        st.image(url)

    else:
        st.warning("No artist or album match could be found. Try again...")

    st.text_input(
        "Search for",
        help="Enter filter here",
        key="search",
        placeholder="Enter the search term and press enter...",
    )
