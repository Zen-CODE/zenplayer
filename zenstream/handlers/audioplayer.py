import streamlit as st
from pathlib import Path
from mutagen import File
from glob import glob
from os import sep
from handlers.imageviewer import ImageViewer

class AudioPlayer:

    @staticmethod
    def _show_meta(file_name: str):

        st.subheader("Track Metadata")
        cols = st.columns([0.1, 0.9])
        info: File = File(file_name).info
        parts = file_name.split(sep)

        for prop, value in [
            ("Artist", parts[-3]),
            ("Album", parts[-2]),
            ("Track", parts[-1]),
            ("Length", f"{int(info.length // 60)}m {int(info.length % 60)}s"),
            ("Bitrate", f"{info.bitrate // 1000}kbps"),
            ("Bitrate mode", AudioPlayer._get_bitrate(info)),
            ("Channels", info.channels),
            ("Sample_rate", f"{info.sample_rate}hz"),
        ]:
            with cols[0]:
                st.markdown(f"**{prop}:**")
            with cols[1]:
                st.markdown(f"*{value}*")


    @staticmethod
    def show_file(file_name: str):
        """Display the audio player, metadata and cover image."""

        st.header("Player")
        st.audio(file_name, autoplay=True)

        if file_name.lower().endswith(".mp3"):
            AudioPlayer._show_meta(file_name)
            AudioPlayer._show_cover(file_name)



    @staticmethod
    def _get_bitrate(info_obj: File) -> str:
        """
        Return the bitrate description given the mutagen bitrate object.
        """
        bitrate_mode = getattr(info_obj, "bitrate_mode", None)
        if bitrate_mode is None:
            return "unknown"
        val = int(bitrate_mode)
        return ["Unknown", "CBR", "VBR", "ABR"][val]

    @staticmethod
    def _show_cover(file_name: str):
        def get_image() -> str:
            parts = file_name.split(sep)
            for ext in ["*.jpg", "*.jpg", "*.png", "*.bmp"]:
                path = sep.join(parts[:-1]) + sep + ext
                for image in glob(path):
                    return image

        image_path = get_image()
        if image_path:
            ImageViewer.show_file(image_path)
