import streamlit as st


class Styler:
    @staticmethod
    def add_header(text: str, image_path: str):
        col1, col2 = st.columns([0.95, 0.05])
        with col1:
            st.markdown(f"## {text}")
        with col2:
            st.image(image_path, width=128)

    st.divider()

    @staticmethod
    def add_row(name: str, value: str):
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            st.markdown(f"**{name}:**")
        with col2:
            st.write(value)
