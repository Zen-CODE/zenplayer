import streamlit as st
from app_pages.zenplayer import get_zenplayer
from app_pages.zenrandom import get_zenrandom
from app_pages.zeninfo import get_zeninfo

# pages = {
#     "ZenPlayer": [
#         st.Page(get_zenplayer, title="Now Playing", icon=":material/play_circle:"),
#         st.Page(get_zenrandom, title="Random Album", icon=":material/shuffle_on:"),
#         st.Page(get_zeninfo, title="Artist Info", icon=":material/info:")
#     ]
# }

# pg = st.navigation(pages)
# pg.run()

pages = {
    "ZenPlayer": get_zenplayer,
    "Random Album": get_zenrandom,
    "Artist Info": get_zeninfo
}

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [key for key in pages.keys()]
)

pages[page]()
