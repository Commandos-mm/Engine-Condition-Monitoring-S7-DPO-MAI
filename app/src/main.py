import streamlit as st

import pipeline

import ui_components as components

from collections import defaultdict

def hack_transform(engine_inference_mapping):
    res = defaultdict(lambda: defaultdict(dict))
    for fk, e in engine_inference_mapping.items():
        for ek, ph in e.items():
            for phk, inf in ph.items():
                res[fk][phk][ek] = inf
    return res

def transform(engine_inference_mapping):
    res = defaultdict(lambda: defaultdict(dict))
    for fk, ph in engine_inference_mapping.items():
        for phk, e in ph.items():
            for ek, inf in e.items():
                res[fk][ek][phk] = inf 
    
    return res

st.set_page_config(
    layout="wide"
)

ts, real_y = components.load_dataset()
pl = pipeline.Pipeline(ts, ground_truth=real_y)
pl.predict()
engine_inference_mapping = pl.get_fmt_data()

engine_inference_mapping = transform(hack_transform(engine_inference_mapping))
with st.spinner():
    for family_id, inference_by_phase in engine_inference_mapping.items():
        components.chart.family_accordion(family_id, inference_by_phase)

