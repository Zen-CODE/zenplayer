import streamlit as st
from state import State
from datetime import datetime


def save_notes(container):
    State.set("notes", st.session_state.get("notes-internal"))
    State.save()
    container.success(f"Notes saved...{datetime.now().isoformat()}")


def show_notes():
    """Show the notes options and buttons."""

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.image("images/notes.jpg", width=128)
    with col1:
        st.markdown("# Notes")
    st.divider()

    col1, col2 = st.columns([0.2, 0.8])

    st.text_area(
        "Notes", value=State.get("notes", ""), key="notes-internal", height=600
    )
    col1.button("Save", on_click=lambda: save_notes(col2))
