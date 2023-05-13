from typing import TypeAlias

import altair as alt
from collections import defaultdict

import streamlit as st
import pandas as pd

import pipeline

from pipeline.predictor import EngineFamily, FlightPhase
import ui_components as components


def transform_inference(dataset) -> dict[EngineFamily, dict[FlightPhase, pd.DataFrame]]:
    res = defaultdict(dict)
    for (phase, family_id), inference in dataset.items():
        res[family_id][phase] = inference
    
    return res



ts = components.load_dataset()

engine_inference_mapping = pipeline.predict(ts)




for family_id, inference_by_phase in transform_inference(engine_inference_mapping).items():
    
    chartl = components.chart.get_chart(inference_by_phase['TAKEOFF'])
    chartr = components.chart.get_chart(inference_by_phase['CRUISE'])

    st.altair_chart(chartl | chartr, theme="streamlit", use_container_width=False)



