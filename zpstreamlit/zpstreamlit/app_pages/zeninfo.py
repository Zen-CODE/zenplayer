import wikipediaapi
from zencore import ZENPLAYER_URL
import requests
import streamlit as st


def get_zeninfo():
    """Show  info about the urrently playing artist"""

    data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
    wiki_wiki = wikipediaapi.Wikipedia("ZenPlayer (zenkey.zencode@gmail.com)", "en")
    page = wiki_wiki.page(data["artist"])

    if page.exists():
        st.markdown(f"# Artist: {data['artist']}")
        st.markdown("## Summary")
        st.write(page.summary)
        st.markdown("## Full Text")
        for part in page.text.split("\n"):
            st.write(part)

    else:
        st.write(f"No information found for *{data['artist']}*")
