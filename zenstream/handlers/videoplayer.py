import streamlit as st


class VideoPlayer:
    @staticmethod
    def show_file(file_name: str):
        """Display the audio player, metadata and cover image."""

        st.header("Video Player")
        st.video(file_name, autoplay=True)
