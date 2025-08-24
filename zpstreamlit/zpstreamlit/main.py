import streamlit as st
from pages.zenplayer import get_zenplayer
from pages.zenrandom import get_zenrandom

pages = {
    "ZenPlayer": [
        st.Page(get_zenplayer, title="Now Playing", icon=":material/play_circle:"),
        st.Page(get_zenrandom, title="Random Album", icon=":material/shuffle_on:")
    ]
}

pg = st.navigation(pages)
pg.run()