from typing import TypeAlias

import altair as alt
from collections import defaultdict

import streamlit as st
import pandas as pd

import pipeline

from pipeline.predictor import EngineFamily, FlightPhase
import ui_components as components


ts = components.load_dataset()

engine_inference_mapping = pipeline.predict(ts)




for (phase, family_id), inference in engine_inference_mapping.items():
    chart = components.chart.get_chart(inference)

    st.altair_chart(chart, theme="streamlit", use_container_width=True)



