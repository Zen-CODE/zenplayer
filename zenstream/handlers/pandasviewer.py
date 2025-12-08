import pandas as pd
import streamlit as st
from styler import Styler


class PandasViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("CSV Viewer")
        st.write(f"File: {file_name}")

        df = pd.read_csv(file_name)
        Styler.show_dataframe("DataFrame", df)
