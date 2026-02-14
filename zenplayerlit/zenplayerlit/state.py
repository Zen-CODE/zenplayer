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
        else:
            st.session_state[name] = value
        State.keys_used.add(name)
        State.save()

    @staticmethod
    def get(name: str, default=""):
        State.keys_used.add(name)
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
        # Save only those value that are not None
        settings_dict = {}
        for key in State.keys_used:
            if value := st.session_state.get(key, None):
                settings_dict[key] = value

        with open("state.json", "w") as f:
            json.dump(
                settings_dict,
                f,
            )
