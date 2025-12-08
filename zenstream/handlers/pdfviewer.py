import streamlit as st
from os.path import sep
import tabula
import pandas as pd
from typing import List


class PDFViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("PDF Viewer")
        st.subheader(file_name.split(sep)[-1])
        with open(file_name, "rb") as f:
            lines = f.read()

        st.pdf(lines)

        dataframes: List[pd.DataFrame] = tabula.read_pdf(file_name)
        if len(dataframes) > 0:
            for index, df in enumerate(dataframes):
                with st.expander(f"Dataframe {index + 1}"):
                    st.data_editor(df, num_rows="dynamic")
        else:
            st.info("No tables found in this PDF.")