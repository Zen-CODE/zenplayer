import wikipediaapi
from zencore import ZENPLAYER_URL
import requests
import streamlit as st
from styler import Styler


def show_zeninfo():
    """Show  info about the urrently playing artist"""

    print("ZenInfo: Fetching wikipedia data...")
    data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
    wiki_wiki = wikipediaapi.Wikipedia("ZenPlayer (zenkey.zencode@gmail.com)", "en")
    page = wiki_wiki.page(data["artist"])

    Styler.add_header("ZenInfo", "images/zencode.jpg")
    if page.exists():
        Styler.add_row("Artist", data["artist"])
        Styler.add_row("Album", data["album"])
        st.markdown("## Summary")
        st.write(page.summary)
        st.markdown("## Full Text")
        [st.write(part) for part in page.text.split("\n")]

    else:
        st.error(f"No information found for *{data['artist']}*")
