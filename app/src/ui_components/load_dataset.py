import streamlit as st
import pandas as pd


def load_dataset() -> pd.DataFrame:
    _, col, _ = st.columns([1, 12, 1])
    uploaded_file = col.file_uploader("Choose a file")
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file.getvalue())
    else:

        return pd.read_csv('src/pipeline/data/X.csv')
    
    