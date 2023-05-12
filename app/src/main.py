from typing import TypeAlias

import altair as alt
from collections import defaultdict

import streamlit as st
import pandas as pd

import pipeline

from pipeline.predictor import EngineFamily, FlightPhase


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    ts = pd.read_csv(uploaded_file.getvalue())
else:
    idx = pd.date_range("2018-01-01", periods=5, freq="H")
    ts = pd.Series(range(len(idx)), index=idx)


st.line_chart(ts)

ts = pd.read_csv('src/pipeline/data/X.csv')
engine_inference_mapping = pipeline.predict(ts)




for (phase, family_id), inference in engine_inference_mapping.items():
    
    metric_column_names = {'ZT49_D'}

        
        
    drawing_dataset = inference[['flight_datetime', *metric_column_names]].astype({'flight_datetime': 'datetime64[ns]'})
    print(drawing_dataset.dtypes)
    chart = alt.Chart(drawing_dataset).mark_circle().encode(
    x='flight_datetime:T',
    y='ZT49_D:Q',
    # color='Origin',
).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)



