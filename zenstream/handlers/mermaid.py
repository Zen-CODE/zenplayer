import streamlit as st
import streamlit_mermaid as mermaid


class MermaidViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("Mermaid Viewer")
        st.write(f"File: {file_name}")
        with open(file_name, "r") as f:
            mermaid.st_mermaid(f.read())
