import streamlit as st


class Styler:

    @staticmethod
    def show_dict(subheader: str, data: dict):
        cols = st.columns([0.1, 0.9])
        for prop, value in data:
            with cols[0]:
                st.markdown(f"**{prop}:**")
            with cols[1]:
                st.markdown(f"*{value}*")
