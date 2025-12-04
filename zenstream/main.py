import streamlit as st
from pathlib import Path
from os import listdir
from os.path import join


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
    def _parent_folder_button(container):
        parent = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                "..",
                icon=":material/arrow_circle_up:",
                on_click=lambda: Action.set_folder(parent),
            )

    @staticmethod
    def _add_this_folder_button(container):
        this_folder = str(Path(State.get_current_folder() + "/../").resolve())
        with container:
            st.button(
                ".",
                icon=":material/adjust:",
                on_click=lambda: Action.set_folder(this_folder),
            )

    @staticmethod
    def _add_folder_button(container, folder):
        with container:
            st.button(
                folder,
                icon=":material/adjust:",
                on_click=lambda: Action.set_folder(folder),
            )

    @staticmethod
    def _add_file_button(container, file_name):
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
                # with cols[(index + 2) % len(cols)]:
                if final_path.is_dir():
                    Show._add_folder_button(cols[(index + 2) % len(cols)], file_name)
                else:
                    Show._add_file_button(cols[(index + 2) % len(cols)], file_name)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Zen File",
        page_icon="ui_assets/discovery_logo.png",
        layout="wide",
    )

    Show.header()
    Show.status()
    Show.listing()
