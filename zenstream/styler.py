import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class Styler:
    @staticmethod
    def show_dict(subheader: str, data: dict):
        st.subheader(subheader)

        cols = st.columns([0.1, 0.9])
        for prop, value in data.items():
            with cols[0]:
                st.markdown(f"**{prop}:**")
            with cols[1]:
                st.markdown(f"*{value}*")

    @staticmethod
    def add_button(container: DeltaGenerator, text: str, icon: str, on_click: callable):
        with container:
            st.button(
                text,
                icon=icon,
                on_click=on_click,
            )
