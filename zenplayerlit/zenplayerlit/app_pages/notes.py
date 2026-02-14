import streamlit as st


def show_notes():
    """Show the notes options and buttons."""

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.image("images/notes.jpg", width=128)
    with col1:
        st.markdown("# Notes")
    st.divider()
    st.button("Save")
    st.text_area("Notes", key="notes")
