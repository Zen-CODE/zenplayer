import streamlit as st
from pathlib import Path
from os.path import sep


class TextViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("Text Viewer")
        st.subheader("Contents: " + file_name.split(sep)[-1])
        with open(file_name, "r") as f:
            lines = "\n".join(f.readlines())

        st.markdown("---")
        match Path(file_name).suffix.lower():
            case ".md":
                st.markdown(lines)
            case ".py":
                st.code(lines)
            case _:
                st.write(lines)
        st.markdown("---")