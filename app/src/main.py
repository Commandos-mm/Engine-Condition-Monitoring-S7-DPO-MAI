import streamlit as st

import pipeline

import ui_components as components

st.set_page_config(
    layout="wide"
)

ts = components.load_dataset()

pl = pipeline.Pipeline(ts)
pl.predict()
engine_inference_mapping = pl.get_fmt_data()

for family_id, inference_by_phase in engine_inference_mapping.items():
    components.chart.family_accordion(family_id, inference_by_phase)

