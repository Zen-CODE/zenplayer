import pandas as pd
import streamlit as st


class PandasViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("Pandas CSV Viewer")
        st.write(f"File: {file_name}")

        df = pd.read_csv(file_name)
        st.data_editor(df, num_rows="dynamic")
