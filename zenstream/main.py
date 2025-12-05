import streamlit as st
from pathlib import Path
from os import listdir, sep
from os.path import join, exists
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
            if not hasattr(st.session_state, "current_folder")
            else Path(st.session_state.current_folder)
        )
        st.session_state.current_folder = path
        return path

    @staticmethod
    def set_current_file(file_name: str):
        st.session_state.current_file = file_name
        [handler.show() for handler in Action.active_handlers]

    @staticmethod
    def get_current_file() -> str:
        return getattr(st.session_state, "current_file", "")



class PandasViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("Pandas CSV Viewer")
        st.write(f"File: {file_name}")

        df = pd.read_csv(file_name)
        st.data_editor(df, num_rows="dynamic")


class TextViewer:

    @staticmethod
    def show_file(file_name: str):

        st.header("Text Viewer")
        st.subheader("Contents: " + file_name.split(sep)[-1])
        with open(file_name, "r") as f:
            lines = "\n".join(f.readlines())

        st.markdown("---")
        match Path(file_name).suffix.lower():
            case ".md":
                st.markdown(lines)
            case ".py":
                st.code(lines)
            case _:
                st.write(lines)
        st.markdown("---")



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
            ("Bitrate mode", Show._get_bitrate(info)),
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
            AudioPlayer._show_meta()
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
            st.subheader("Cover Image")
            st.image(image_path)

class Action:

    handlers = {".mp3" : [AudioPlayer],
                ".ogg": [AudioPlayer] ,
                ".wav": [AudioPlayer],
                ".csv": [PandasViewer],
                ".txt": [TextViewer],
                ".py": [TextViewer],
                ".ini": [TextViewer],
                ".yaml": [TextViewer],
                ".yml": [TextViewer],
                ".md": [TextViewer],
                }

    """A dictionary of file type / handler class list pairs. The handler class
    exposing a `show()` method."""

    active_handlers = []
    """A list of handlers for the file to be called after the main listing"""

    @staticmethod
    def set_current_folder(current_folder: str):
        print(f"set_current_folder - {current_folder}")
        st.session_state.current_folder = current_folder
        Action.active_handlers = []

    @staticmethod
    def set_file(file_name: str):
        print(f"Action.set_file({file_name})")
        st.session_state.current_file = file_name
        if file_name:
            file_type = Path(file_name).suffix.lower()
            for handler in Action.handlers.get(file_type, []):
                handler.show_file(file_name)


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
        st.text(f"Current file: {State.get_current_file()}")

    @staticmethod
    def _parent_folder_button(container: DeltaGenerator):
        parent = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                "<<",
                icon=":material/arrow_circle_up:",
                on_click=lambda: Action.set_current_folder(parent),
            )

    @staticmethod
    def _add_this_folder_button(container: DeltaGenerator):
        this_folder = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                "<",
                icon=":material/adjust:",
                on_click=lambda: Action.set_current_folder(this_folder),
            )

    @staticmethod
    def _add_folder_button(container: DeltaGenerator, text: str, folder: str):
        with container:
            st.button(
                text,
                icon=":material/adjust:",
                on_click=lambda: Action.set_current_folder(folder),
            )

    @staticmethod
    def _add_file_button(container: DeltaGenerator, file_name: str, folder: str):
        with container:
            st.button(
                file_name,
                icon=":material/adjust:",
                on_click=lambda: Action.set_file(sep.join([folder, file_name])),
            )

    @staticmethod
    def listing():
        st.header("Listing")
        with st.container():
            cols = st.columns([0.25] * 4)
            Show._parent_folder_button(cols[0])
            Show._add_this_folder_button(cols[1])

            folder = st.session_state.current_folder
            for index, file_name in enumerate(sorted(listdir(folder))):
                final_path = Path(join(folder, file_name))
                if final_path.is_dir():
                    Show._add_folder_button(
                        cols[(index + 2) % len(cols)], file_name, str(final_path)
                    )
                else:
                    Show._add_file_button(
                        cols[(index + 2) % len(cols)], file_name, folder
                    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Zen File",
        page_icon="ui_assets/discovery_logo.png",
        layout="wide",
    )

    Show.header()
    Show.status()
    Show.listing()
    print("handlers = ", Action.active_handlers)
    # [handler.show() for handler in Action.active_handlers]
    # Show.now_playing()
