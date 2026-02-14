import streamlit as st

from os.path import exists
import json


class State:
    keys_used = set()

    @staticmethod
    def set(name: str, value: str | None):
        """Set the value of key in the state dictionary. Remove if None."""
        if value is None:
            if name in st.session_state.keys():
                st.session_state.pop(name)
            State.keys_used.remove(name)
        else:
            st.session_state[name] = value
            State.keys_used.add(name)
        State.save()

    @staticmethod
    def get(name: str, default=""):
        return st.session_state.get(name, default)

    @staticmethod
    def load():
        if exists("state.json"):
            with open("state.json") as f:
                values = json.load(f)
            for key, value in values.items():
                setattr(st.session_state, key, value)

    @staticmethod
    def save():
        settings_dict = {k: st.session_state.get(k) for k in State.keys_used}

        with open("state.json", "w") as f:
            json.dump(
                # {
                #     "current_folder": st.session_state.get("current_folder", ""),
                #     "current_file": st.session_state.get("current_file", ""),
                # },
                settings_dict,
                f,
            )
