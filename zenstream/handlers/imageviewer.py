import streamlit as st
from PIL import Image



class ImageViewer:

    @staticmethod
    def show_file(file_name: str):
        """Display the image."""

        st.header("Image Viewer")
        st.subheader("Image")
        st.image(file_name)
        st.subheader("Metadata")
        col1, col2 = st.columns([0.2, 0.8])
        for key, value in ImageViewer._get_metadata(file_name).items():
            col1.markdown(f"**{key}**")
            col2.markdown(value)


    @staticmethod
    def _get_metadata(file_name: str) -> dict:

        with Image.open(file_name) as img:
            return {"Format": img.format,
                    "Dimensions (W, H)": f"{img.size} pixels",
                    "Color Mode": img.mode}
