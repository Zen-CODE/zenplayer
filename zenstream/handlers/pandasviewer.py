import pandas as pd
import streamlit as st


class PandasViewer:
    @staticmethod
    def show_file(file_name: str):
        st.header("Pandas CSV Viewer")
        st.write(f"File: {file_name}")

        df = pd.read_csv(file_name)
        st.data_editor(df, num_rows="dynamic")

        # Try adding some graphs
        col1, col2 = st.columns(2)
        st.divider()
        st.markdown("CSV analysis")
        with col1:
            st.markdown("**Area Chart**")
            st.area_chart(df)
            st.markdown("**Bar Chart**")
            st.bar_chart(df)
        with col2:
            st.markdown("**Line Chart**")
            st.line_chart(df)
