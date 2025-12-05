import streamlit as st
from pathlib import Path
from os import listdir, sep
from os.path import join
from streamlit.delta_generator import DeltaGenerator
from handlers.pandasviewer import PandasViewer
from handlers.textviewer import TextViewer
from handlers.audioplayer import AudioPlayer
from handlers.imageviewer import ImageViewer
from handlers.pdfviewer import PDFViewer
from styler import Styler


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

    @staticmethod
    def get_current_file() -> str:
        return getattr(st.session_state, "current_file", "")


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
                ".bat": [TextViewer],
                ".sh": [TextViewer],
                ".md": [TextViewer],
                ".json": [TextViewer],
                ".pdf": [PDFViewer],
                ".toml": [TextViewer],
                ".jpeg": [ImageViewer],
                ".jpg": [ImageViewer],
                ".png": [ImageViewer],
                }
    """A dictionary of file type / handler class list pairs. The handler class
    exposing a `show_file(file_name)` method."""

    @staticmethod
    def set_current_folder(current_folder: str):
        print(f"set_current_folder - {current_folder}")
        st.session_state.current_folder = current_folder

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
        st.markdown(f"**Current directory:** {State.get_current_folder()}")
        st.markdown(f"**Current file:** {State.get_current_file()}")

    @staticmethod
    def _parent_folder_button(container: DeltaGenerator):
        parent = str(Path(State.get_current_folder() + "/../").resolve())
        Styler.add_button(container, "<<",":material/arrow_circle_up:",
                          lambda: Action.set_current_folder(parent))

    @staticmethod
    def _add_folder_button(container: DeltaGenerator, text: str, folder: str):
        Styler.add_button(container, text,":material/folder:",
                          lambda: Action.set_current_folder(folder))

    @staticmethod
    def _add_file_button(container: DeltaGenerator, file_name: str, folder: str):
        Styler.add_button(container, file_name,":material/article:",
                lambda: Action.set_file(sep.join([folder, file_name])))

    @staticmethod
    def listing():
        st.header("Listing")
        with st.container():
            cols = st.columns([0.25] * 4)
            Show._parent_folder_button(cols[0])

            folder = st.session_state.current_folder
            for index, file_name in enumerate(sorted(listdir(folder))):
                final_path = Path(join(folder, file_name))
                if final_path.is_dir():
                    Show._add_folder_button(
                        cols[(index + 1) % len(cols)], file_name, str(final_path)
                    )
                else:
                    Show._add_file_button(
                        cols[(index + 1) % len(cols)], file_name, folder
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
