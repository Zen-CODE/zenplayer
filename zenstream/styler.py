import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd


class Styler:
    @staticmethod
    def show_dict(subheader: str, data: dict):
        st.subheader(subheader)

        cols = st.columns([0.1, 0.9])
        for prop, value in data.items():
            with cols[0]:
                st.markdown(f"**{prop}:**")
            with cols[1]:
                st.markdown(f"*{value}*")

    @staticmethod
    def add_button(container: DeltaGenerator, text: str, icon: str, on_click: callable):
        with container:
            st.button(
                text,
                icon=icon,
                on_click=on_click,
            )

    @staticmethod
    def show_dataframe(text: str, df: pd.DataFrame):
        with st.expander(text):
            st.markdown("Dataframe analysis")
            col1, col2 = st.columns(2)
            try:
                with col1:
                    st.markdown("**Area Chart**")
                    st.area_chart(df)
                    st.markdown("**Bar Chart**")
                    st.bar_chart(df)
                with col2:
                    st.markdown("**Line Chart**")
                    st.line_chart(df)
            except Exception as e:
                with col1:
                    st.error(
                        f"The DataFrame could not be graphed. It gave the error: {e}"
                    )
