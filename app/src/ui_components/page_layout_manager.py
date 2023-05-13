import streamlit as st


class PageLayout:
    def __init__(self):
        _, self.center, _ = st.columns([1, 12, 1])

    def __enter__(self):
        return self.center

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        pass
