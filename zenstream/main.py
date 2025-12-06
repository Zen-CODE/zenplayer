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
from handlers.videoplayer import VideoPlayer
from handlers.excelviewer import ExcelViewer
from handlers.docxviewer import DocXViewer
from styler import Styler
from handlers.filedetails import FileDetails
import webbrowser
import pyperclip


class State:
    @staticmethod
    def get_current_folder() -> str:
        path = str(
            Path.cwd()
            if not hasattr(st.session_state, "current_folder")
            else Path(st.session_state.current_folder)
        )
        st.session_state.current_folder = path
        return path

    @staticmethod
    def set_current_file(file_name: str | None):
        st.session_state.current_file = None

    @staticmethod
    def get_current_file() -> str:
        return getattr(st.session_state, "current_file", "")


class Action:
    handlers = {
        "mp3": [AudioPlayer],
        "ogg": [AudioPlayer],
        "wav": [AudioPlayer],
        "csv": [PandasViewer],
        "txt": [TextViewer],
        "py": [TextViewer],
        "log": [TextViewer],
        "ini": [TextViewer],
        "yaml": [TextViewer],
        "yml": [TextViewer],
        "bat": [TextViewer],
        "sh": [TextViewer],
        "md": [TextViewer],
        "json": [TextViewer],
        "pdf": [PDFViewer],
        "toml": [TextViewer],
        "jpeg": [ImageViewer],
        "jpg": [ImageViewer],
        "png": [ImageViewer],
        "webm": [VideoPlayer],
        "mp4": [VideoPlayer],
        "avi": [VideoPlayer],
        "xls": [ExcelViewer],
        "xlsx": [ExcelViewer],
        "docx": [DocXViewer],
    }
    """A dictionary of file type / handler class list pairs. The handler class
    exposing a `show_file(file_name)` method."""

    @staticmethod
    def get_handlers(file_name: str) -> list:
        ext = file_name.split(".")[-1]
        return Action.handlers.get(ext, [])

    @staticmethod
    def get_icon(file_name: str) -> str:
        suffix = file_name.split(".")[-1]
        match suffix:
            case "mp3" | "ogg" | "wav":
                return ":material/audio_file:"
            case "csv":
                return ":material/csv:"
            case "txt" | "md":
                return ":material/text_snippet:"
            case "py":
                return ":material/code:"
            case "ini" | "yaml" | "yml" | "json" | "toml":
                return ":material/settings:"
            case "bat" | "sh":
                return ":material/run_circle:"
            case "pdf":
                return ":material/picture_as_pdf:"
            case "jpeg" | "jpg" | "png":
                return ":material/image:"
            case "webm" | "mp4" | "avi":
                return ":material/movie:"
            case "xls" | "xlsx":
                return ":material/table:"
            case "log":
                return ":material/history_toggle_off:"
            case "docx":
                return ":material/dictionary:"
            case _:
                return ":material/article:"

    @staticmethod
    def set_current_folder(current_folder: str):
        st.session_state.current_folder = current_folder

    @staticmethod
    def set_file(file_name: str):
        st.session_state.current_file = file_name


class Show:
    @staticmethod
    def header():
        with st.container():
            col1, col2 = st.columns([0.96, 0.04])
            with col1:
                st.title("💧 ZenStream - File explorer, viewer and extractor")
            with col2:
                st.image("images/favicon.png")

    @staticmethod
    def _parent_folder_button(container: DeltaGenerator):
        parent = str(Path(State.get_current_folder() + "/../").resolve())
        Styler.add_button(
            container,
            "<- 💧",
            ":material/arrow_circle_up:",
            lambda: Action.set_current_folder(parent),
        )

    @staticmethod
    def _add_folder_button(container: DeltaGenerator, text: str, folder: str):
        Styler.add_button(
            container,
            text,
            ":material/folder:",
            lambda: Action.set_current_folder(folder),
        )

    @staticmethod
    def _add_file_button(container: DeltaGenerator, file_name: str, folder: str):
        Styler.add_button(
            container,
            file_name,
            Action.get_icon(file_name),
            lambda: Action.set_file(sep.join([folder, file_name])),
        )

    @staticmethod
    def listing():
        folder = State.get_current_folder()
        # st.header("Listing")
        st.info(f"Current directory: {folder}")
        with st.container():
            cols = st.columns([0.25] * 4)
            Show._parent_folder_button(cols[0])

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
        st.divider()

    @staticmethod
    def details():
        if file_name := State.get_current_file():
            # Add buttons for Open, Copy and Clear
            col1, col2, col3, col4 = st.columns([0.8, 0.1, 0.1, 0.1])
            with col1:
                st.info(f"Current file: {file_name}")
            Styler.add_button(
                col2,
                "Copy path",
                on_click=lambda *args: pyperclip.copy(file_name),
                icon=":material/content_copy:",
            )
            Styler.add_button(
                col3,
                "Open file",
                on_click=lambda *args: webbrowser.open(file_name),
                icon=":material/open_in_full:",
            )
            Styler.add_button(
                col4,
                "Clear",
                on_click=lambda *args: State.set_current_file(None),
                icon=":material/close:",
            )

            for handler in Action.get_handlers(file_name):
                handler.show_file(file_name)
                st.divider()

            with st.expander("File details"):
                FileDetails.show_file(file_name)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Zen Stream", page_icon="images/favicon.png", layout="wide"
    )

    Show.header()
    Show.listing()
    Show.details()
    st.markdown('“Be like water." - *Bruce Lee*')
