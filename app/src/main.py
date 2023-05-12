from typing import TypeAlias

import altair as alt
from collections import defaultdict

import streamlit as st
import pandas as pd

import pipeline

from pipeline.predictor import EngineFamily, FlightPhase
from ui_components.chart import get_chart


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    ts = pd.read_csv(uploaded_file.getvalue())
else:

    ts = pd.read_csv('src/pipeline/data/X.csv')

engine_inference_mapping = pipeline.predict(ts)




for (phase, family_id), inference in engine_inference_mapping.items():
    chart = get_chart(inference)

    st.altair_chart(chart, theme="streamlit", use_container_width=True)



