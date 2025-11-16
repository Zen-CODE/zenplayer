import wikipediaapi
from zencore import ZENPLAYER_URL
import requests
import streamlit as st


def get_zeninfo():
    """Show  info about the urrently playing artist"""

    print("ZenInfo: Fetching wikipedia data...")
    data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
    wiki_wiki = wikipediaapi.Wikipedia("ZenPlayer (zenkey.zencode@gmail.com)", "en")
    page = wiki_wiki.page(data["artist"])

    container = st.container()
    if page.exists():
        container.markdown(f"# Artist: {data['artist']}")
        container.markdown("## Summary")
        container.write(page.summary)
        container.markdown("## Full Text")
        for part in page.text.split("\n"):
            container.write(part)

    else:
        container.write(f"No information found for *{data['artist']}*")
