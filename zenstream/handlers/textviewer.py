import streamlit as st
from pathlib import Path
from os.path import sep


class TextViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("Text Viewer")
        st.subheader("Contents: " + file_name.split(sep)[-1])
        with open(file_name, "r") as f:
            lines = f.read()

        st.markdown("---")
        if Path(file_name).suffix.lower() == ".md":
            st.markdown(lines)
        else:
            st.code(lines, line_numbers=True,)
        st.markdown("---")
