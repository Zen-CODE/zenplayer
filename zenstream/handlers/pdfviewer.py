import streamlit as st
from pathlib import Path
from os.path import sep


class PDFViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("PDF Viewer")
        st.subheader(file_name.split(sep)[-1])
        with open(file_name, "rb") as f:
            lines = f.read()

        st.divider()
        st.pdf(lines)
        st.divider()
