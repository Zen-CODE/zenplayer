from handlers.pandasviewer import PandasViewer
from handlers.textviewer import TextViewer
from handlers.audioplayer import AudioPlayer
from handlers.imageviewer import ImageViewer
from handlers.pdfviewer import PDFViewer
from handlers.videoplayer import VideoPlayer
from handlers.excelviewer import ExcelViewer
from handlers.docxviewer import DocXViewer
from pathlib import Path
import streamlit as st
from state import State
import subprocess
import sys


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
        "sql": [TextViewer],
        "crt": [TextViewer],
        "sh": [TextViewer],
        "ipynb": [TextViewer],
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
    def delete_file(file_name: str):
        try:
            Path(file_name).unlink(missing_ok=True)
        except Exception as e:
            st.error(f"Error deleting file: {e}")

        State.set("current_file", "")
        State.set("delete_file", "")

    @staticmethod
    def run_file(file_name: str):
        """Run the given file. Currently, only python files are supported."""
        print(f"Running {file_name}")
        match file_name.split(".")[-1].lower():
            case "py":
                PythonFile.run(file_name)
            case _:
                return []


class PythonFile:

    @staticmethod
    def run(file_name: str):
        subprocess.run(
            [sys.executable, file_name],
            stderr=subprocess.PIPE,
            check=True,
            # env=os.environ.copy(),
            encoding='utf-8'
        )

