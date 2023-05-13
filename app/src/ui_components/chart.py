import streamlit as st
import altair as alt
import pandas as pd

from .page_layout_manager import PageLayout

metric_column_names = {'ZT49_D'}

def family_page_info(engine_family_id, family_inference):
    engine_id = st.selectbox(
        'Engine ID',
        tuple(family_inference.keys()),
        key = engine_family_id
    )
    engine_graphics(family_inference[engine_id])


def engine_graphics(engine_inference):
    chartl = get_chart(engine_inference['TAKEOFF'])
    chartr = get_chart(engine_inference['CRUISE'])
    with PageLayout() as page:
        page.altair_chart(chartl | chartr, theme="streamlit", use_container_width=True)


def family_accordion(engine_family_id: str, family_inference: dict):
    with st.expander(f'Engine family: {engine_family_id}'):
        family_page_info(engine_family_id, family_inference)

def get_chart(dataset: pd.DataFrame) -> alt.Chart:
    drawing_dataset = (
        dataset[['flight_datetime', *metric_column_names]]
        .astype({'flight_datetime': 'datetime64[ns]'})
    )

    chart = (
        alt.Chart(drawing_dataset)
        .mark_circle()
        .encode(
            x='flight_datetime:T',
            y=f'ZT49_D:Q',
        )
        .interactive()
    )
    return chart
