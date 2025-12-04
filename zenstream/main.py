import streamlit as st
from pathlib import Path
from os import listdir, sep
from os.path import join
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
from mutagen import File
from glob import glob


class State:
    @staticmethod
    def get_current_folder() -> str:
        """Return the full path to the current folder"""
        path = str(
            Path.cwd()
            if not hasattr(st.session_state, "folder")
            else Path(st.session_state.folder)
        )
        st.session_state.folder = path
        return path


class Action:
    @staticmethod
    def open_file(file_name):
        print(f"open_file - {file_name}")

    @staticmethod
    def set_folder(folder):
        print(f"set_folder - {folder}")
        st.session_state.folder = folder

    @staticmethod
    def set_file(file_name):
        print(f"set_file - {file_name}")


class Show:
    @staticmethod
    def header():
        with st.container():
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.title("ZenStream")
            with col2:
                image_path = str(Path("./images/main.png").resolve())
                st.image(image_path)

    @staticmethod
    def status():
        st.header("Status")
        st.text(f"Current directory: {State.get_current_folder()}")

    @staticmethod
    def _parent_folder_button(container: DeltaGenerator):
        parent = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                "..",
                icon=":material/arrow_circle_up:",
                on_click=lambda: Action.set_folder(parent),
            )

    @staticmethod
    def _add_this_folder_button(container: DeltaGenerator):
        this_folder = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                ".",
                icon=":material/adjust:",
                on_click=lambda: Action.set_folder(this_folder),
            )

    @staticmethod
    def _add_folder_button(container: DeltaGenerator, folder: str):
        with container:
            st.button(
                folder,
                icon=":material/adjust:",
                on_click=lambda: Action.set_folder(folder),
            )

    @staticmethod
    def _add_file_button(container: DeltaGenerator, file_name: str):
        with container:
            st.button(
                file_name,
                icon=":material/adjust:",
                on_click=lambda: Action.set_file(file_name),
            )

    @staticmethod
    def listing():
        st.header("Listing")
        with st.container():
            cols = st.columns([0.25] * 4)
            Show._parent_folder_button(cols[0])
            Show._add_this_folder_button(cols[1])

            for index, file_name in enumerate(sorted(listdir(st.session_state.folder))):
                final_path = Path(join(st.session_state.folder, file_name))
                if final_path.is_dir():
                    Show._add_folder_button(cols[(index + 2) % len(cols)], file_name)
                else:
                    Show._add_file_button(cols[(index + 2) % len(cols)], file_name)

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
    def now_playing():
        st.header("Now Playing")

        df = pd.read_csv(
            "/home/richard/.zencode/zenplayer/nowplaying.csv",
        )
        df = df.drop(["machine"], axis=1)
        st.data_editor(df, num_rows="dynamic")

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
            st.subheader("Cover Image")
            st.image(image_path)

    @staticmethod
    def player():
        st.header("Player")
        file_name = "/home/richard/Zen/Music/Dead By April/Let the World Know/01 - Beautiful Nightmare.mp3"
        st.audio(file_name, autoplay=True)

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
            ("Bitrate mode", Show._get_bitrate(info)),
            ("Channels", info.channels),
            ("Sample_rate", f"{info.sample_rate}hz"),
        ]:
            with cols[0]:
                st.markdown(f"**{prop}:**")
            with cols[1]:
                st.markdown(f"*{value}*")

        Show._show_cover(file_name)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Zen File",
        page_icon="ui_assets/discovery_logo.png",
        layout="wide",
    )

    Show.header()
    Show.status()
    Show.listing()
    # Show.now_playing()
    Show.player()
