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
    def listing():
        st.header("Listing")
        with st.container():
            cols = st.columns([0.25] * 4)

            # Add this folder and partent
            up_one = str(Path(State.get_current_folder() + "/../").resolve())
            with cols[0]:
                st.button(
                    "..",
                    icon=":material/arrow_circle_up:",
                    on_click=lambda: Action.set_folder(up_one),
                )
            # Add this folder and partent
            this_folder = str(Path(State.get_current_folder() + "/../").resolve())
            with cols[1]:
                st.button(
                    ".",
                    icon=":material/arrow_circle_up:",
                    on_click=lambda: Action.set_folder(this_folder),
                )

            for index, file_name in enumerate(listdir(st.session_state.folder)):
                final_path = Path(join(st.session_state.folder, file_name))
                with cols[(index + 2) % len(cols)]:
                    if final_path.is_dir():
                        st.button(
                            f">> {file_name}",
                            icon=":material/folder:",
                            on_click=lambda f_name=str(final_path): Action.set_folder(
                                f_name
                            ),
                        )
                    else:
                        st.button(
                            file_name,
                            icon=":material/file_export:",
                            on_click=lambda f_name=str(file_name): Action.open_file(
                                f_name
                            ),
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
