import streamlit as st

import pipeline

import ui_components as components

st.set_page_config(
    layout="wide"
)

ts = components.load_dataset()

engine_inference_mapping = pipeline.predict(ts)

# TODO: remove
HARDCODED_ENGINE_FAMILY: str = "CFM56-7"
HARDCODED_ENGINE_ID: str = "364a94e57c5e7705c650bdadda955186d3a8f9d96a3d9ec0f32964ef9c09b494"

single_inference = engine_inference_mapping[HARDCODED_ENGINE_FAMILY][HARDCODED_ENGINE_ID]
chart_takeoff = components.chart.get_chart(single_inference['TAKEOFF'])
chart_cruise = components.chart.get_chart(single_inference['CRUISE'])
with components.PageLayout() as page:
    page.altair_chart(chart_takeoff | chart_cruise, theme="streamlit", use_container_width=True)
