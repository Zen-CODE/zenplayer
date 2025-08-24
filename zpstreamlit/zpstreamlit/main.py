import streamlit as st
from pages.zenplayer import get_zenplayer
from pages.zencurrent import get_zencurrent

pages = {
    "ZenPlayer": [
        st.Page(get_zenplayer, title="Now Playing"),
        st.Page(get_zencurrent, title="Current Track")
    ]
}

pg = st.navigation(pages)
pg.run()