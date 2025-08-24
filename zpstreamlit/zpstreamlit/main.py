import streamlit as st
from pages.zenplayer import get_zenplayer
from pages.zenlibrary import get_zenlibrary

pages = {
    "ZenPlayer": [
        st.Page(get_zenplayer, title="Now playing"),
        st.Page(get_zenlibrary, title="Library")
    ]
}

pg = st.navigation(pages)
pg.run()