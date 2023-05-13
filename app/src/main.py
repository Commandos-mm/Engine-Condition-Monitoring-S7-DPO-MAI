import streamlit as st

import pipeline

import ui_components as components

st.set_page_config(
    layout="wide"
)

ts = components.load_dataset()

engine_inference_mapping = pipeline.predict(ts)

for family_id, inference_by_phase in engine_inference_mapping.items():
    components.chart.family_accordion(family_id, inference_by_phase)

