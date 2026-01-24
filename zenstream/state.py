import streamlit as st
from pathlib import Path
from os.path import exists
import json


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
    def set(name: str, value: str):
        st.session_state[name] = value
        if name == "current_folder":
            if st.session_state.get("current_file"):
                st.session_state.pop("current_file")
        State.save()

    @staticmethod
    def get(name: str):
        return st.session_state.get(name, "")

    @staticmethod
    def load():
        if exists("state.json"):
            with open("state.json") as f:
                values = json.load(f)
            for key, value in values.items():
                setattr(st.session_state, key, value)

    @staticmethod
    def save():
        with open("state.json", "w") as f:
            json.dump(
                {
                    "current_folder": st.session_state.get("current_folder", ""),
                    "current_file": st.session_state.get("current_file", ""),
                },
                f,
            )
