import streamlit as st
from time import sleep


def show_musiclib():
    for i in range(10):
        with st.spinner("Loading {i}"):
            st.button(f"Button {i}")
            sleep(1)

    st.write("Okay, we are done")
