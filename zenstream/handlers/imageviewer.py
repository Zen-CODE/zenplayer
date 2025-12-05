import streamlit as st
from PIL import Image, ImageFile
from PIL.ExifTags import TAGS
from styler import Styler


class ImageViewer:
    @staticmethod
    def show_file(file_name: str):
        """Display the image."""

        st.header("Image Viewer")
        st.subheader("Image")
        st.image(file_name)

        with Image.open(file_name) as img:
            image_data = ImageViewer._get_metadata(img)
            Styler.show_dict("Image metadata", image_data)
            exif_data = ImageViewer._get_exif_data(img)
            if exif_data:
                Styler.show_dict("Camera information", exif_data)

    @staticmethod
    def _get_metadata(img: ImageFile) -> dict:
        return {
            "Format": img.format,
            "Dimensions (W, H)": f"{img.size} pixels",
            "Color Mode": img.mode,
        }

    @staticmethod
    def _get_exif_data(img: ImageFile) -> dict:
        exif_data = img.getexif()
        if exif_data:
            tags = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)  # Get human-readable name or use ID
                tags[tag_name.title()] = str(value)
            return tags

        return {}
