import streamlit as st
from pathlib import Path
from os import listdir, sep
from os.path import join
from streamlit.delta_generator import DeltaGenerator
from styler import Styler
from handlers.filedetails import FileDetails
import webbrowser
import pyperclip
from styler import NUM_COLUMNS
from actions import Action
from state import State
from functools import partial
from uuid import uuid4


class Show:
    @staticmethod
    def header():
        with st.container():
            # First row
            col1, col2 = st.columns([0.96, 0.04])
            col1.title("💧 ZenStream")
            col2.image("images/favicon.png")
            st.divider()

            # Add folder breadcrumbs
            Show._add_path_buttons()
            st.divider()

    @staticmethod
    def _add_path_buttons():
        folder = State.get_current_folder()
        # Yes, we assume linux for now :-)

        parts = folder.split(sep)[1:]
        num_folders = len(parts)
        cols = st.columns(num_folders + 2)  # Add root folder and info tag
        cols[0].info("💧 Current folder")
        cols[1].button(
            "📁",
            key=str(uuid4()),
            width="stretch",
            on_click=partial(State.set, "current_folder", "/")
        )
        if num_folders == 1 and parts[0] == "":
            return

        dest_folder = ""
        for i in range(num_folders):
            dest_folder = dest_folder + sep + parts[i]
            cols[i + 2].button(
                "📁 " + parts[i],
                key=str(uuid4()),
                width="stretch",
                on_click=partial(State.set, "current_folder", dest_folder),
            )

    @staticmethod
    def _add_folder_button(container: DeltaGenerator, text: str, folder: str):
        Styler.add_button(
            container,
            "📁 " + text,
            None,
            lambda: State.set("current_folder", folder),
        )

    @staticmethod
    def _add_file_button(container: DeltaGenerator, file_name: str, folder: str):
        if sep.join([folder, file_name]) == State.get("current_file"):
            text = file_name + " 🟢"
        else:
            text = file_name
        Styler.add_button(
            container,
            text,
            Action.get_icon(file_name),
            lambda: State.set("current_file", sep.join([folder, file_name])),
        )

    @staticmethod
    def _get_extra_buttons(file_name: str) -> list:
        ext = file_name.split(".")[-1].lower()
        match ext:
            case "py":
                return [
                    {
                        "text": "Run script",
                        "icon": ":material/run_circle:",
                        "on_click": lambda *args: Action.run_file(file_name),
                    }
                ]
        return []

    @staticmethod
    def _show_extra_file_buttons(file_name: str):
        button_data = Show._get_extra_buttons(file_name)
        if button_data:
            cols = st.columns(len(button_data) + 1)
            cols[0].info("💧💧💧 Extra options for this file")
            for k, data in enumerate(button_data):
                Styler.add_button(cols[k + 1], **data)

    @staticmethod
    def listing():
        folder = State.get_current_folder()
        with st.container():
            cols = st.columns(NUM_COLUMNS)

            for index, file_name in enumerate(sorted(listdir(folder))):
                final_path = Path(join(folder, file_name))
                if final_path.is_dir():
                    Show._add_folder_button(
                        cols[index % NUM_COLUMNS], file_name, str(final_path)
                    )
                else:
                    Show._add_file_button(cols[index % NUM_COLUMNS], file_name, folder)
        st.divider()

    @staticmethod
    def _confirm_delete(file_name: str):
        st.warning("⚠️ Are you sure you want to delete this file?")
        col_yes, col_no = st.columns(2)
        Styler.add_button(
            col_yes,
            "Delete",
            ":material/delete:",
            lambda *args: Action.delete_file(file_name),
            width="content",
        )
        Styler.add_button(
            col_no,
            "Cancel",
            ":material/close:",
            on_click=lambda *args: State.set("delete_file", ""),
            type="primary",
            width="content",
        )

    @staticmethod
    def _show_file_buttons(file_name: str):
        # Add buttons for Open, Copy, Delete and Clear
        col1, col2, col3, col4, col5 = st.columns([0.5, 0.125, 0.125, 0.125, 0.125])
        with col1:
            st.info(f"💧💧 Current file: {file_name}")
        Styler.add_button(
            col2,
            "Copy path",
            on_click=lambda *args: pyperclip.copy(file_name),
            icon=":material/content_copy:",
        )
        Styler.add_button(
            col3,
            "Open",
            on_click=lambda *args: webbrowser.open(file_name),
            icon=":material/open_in_full:",
        )
        Styler.add_button(
            col4,
            "Delete",
            on_click=lambda *args: State.set("delete_file", file_name),
            icon=":material/delete:",
        )
        Styler.add_button(
            col5,
            "Clear",
            on_click=lambda *args: State.set("current_file", ""),
            icon=":material/delete:",
        )

    @staticmethod
    def details(file_name):
        if del_file := State.get("delete_file"):
            Show._confirm_delete(del_file)
        Show._show_file_buttons(file_name)
        Show._show_extra_file_buttons(file_name)

        for handler in Action.get_handlers(file_name):
            handler.show_file(file_name)

        with st.expander("Details"):
            FileDetails.show_file(file_name)

    @staticmethod
    def show_footer():
        st.markdown('“Be like water..." - *Bruce Lee*')


if __name__ == "__main__":
    st.set_page_config(
        page_title="Zen Stream", page_icon="images/favicon.png", layout="wide"
    )

    State.load()
    Show.header()
    Show.listing()
    if file_name := State.get("current_file"):
        Show.details(file_name)
    Show.show_footer()
