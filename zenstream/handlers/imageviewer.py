import streamlit as st
from PIL import Image, ImageFile



class ImageViewer:

    @staticmethod
    def _show_dict(subheader: str, data: dict):
        st.subheader(subheader)
        col1, col2 = st.columns([0.2, 0.8])
        for key, value in data.items():
            col1.markdown(f"**{key}**")
            col2.markdown(value)

    @staticmethod
    def show_file(file_name: str):
        """Display the image."""

        st.header("Image Viewer")
        st.subheader("Image")
        st.image(file_name)

        with Image.open(file_name) as img:
            image_data = ImageViewer._get_metadata(img)
            ImageViewer._show_dict("Image metadata", image_data)
            exif_data = ImageViewer._get_exif_data(img)
            if exif_data:
                ImageViewer._show_dict("Camera information", exif_data)


    @staticmethod
    def _get_metadata(img: ImageFile) -> dict:
        return {"Format": img.format,
                "Dimensions (W, H)": f"{img.size} pixels",
                "Color Mode": img.mode}

    @staticmethod
    def _get_exif_data(img: ImageFile) -> dict:
        exif_data = img.getexif()
        if exif_data:
            # EXIF_TAGS = {
            #     271: "Make (Camera Brand)",
            #     272: "Model (Camera Model)",
            #     306: "DateTime (Modification Date)",
            #     36867: "DateTimeOriginal (Capture Date)",
            #     33434: "ExposureTime (Shutter Speed)",
            #     33437: "FNumber (Aperture)",
            #     34855: "ISOSpeedRatings",
            # }

            return {"Camera": exif_data.get(271, "-"),
                    "Model": exif_data.get(272, "-"),
                     "Date modified": exif_data.get(306, "-"),
                     "Date original": exif_data.get(36867, "-"),
                     "Exposure time (shutter speed)": exif_data.get(33434, "-"),
                     "Aperture": exif_data.get(33437, "-")}

        return {}