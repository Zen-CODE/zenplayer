import streamlit as st
from pathlib import Path
from os.path import sep


class TextViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("Text Viewer")
        st.subheader(file_name.split(sep)[-1])
        with open(file_name, "r") as f:
            lines = f.read()

        st.divider()
        match Path(file_name).suffix.lower():
            case ".md":
                st.markdown(lines)
            case ".json":
                st.json(lines)
            case _:
                st.code(lines, line_numbers=True,)
        st.divider()
