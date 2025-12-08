import streamlit as st
from os.path import sep
from styler import Styler
import pandas as pd


class TextViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("Text Viewer")
        st.subheader(file_name.split(sep)[-1])

        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.read()

        match file_name.split(".")[-1].lower():
            case "md":
                st.code(
                    lines,
                    line_numbers=True,
                )
                with st.expander("Rendered markdown"):
                    st.markdown(lines)
            case "json":
                st.json(lines)
                try:
                    df = pd.read_json(file_name)
                    Styler.show_dataframe("DataFrame", df)
                except Exception as e:
                    st.warning(
                        f"There was an issue converting this json to a dataframe ({e}).\n"
                        "This is not unusual - json is freeform and not built for tabular data."
                    )
            case _:
                st.code(
                    lines,
                    line_numbers=True,
                )
