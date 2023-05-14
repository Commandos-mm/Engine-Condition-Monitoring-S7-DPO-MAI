import streamlit as st
import altair as alt
import pandas as pd
import streamlit_nested_layout

from .page_layout_manager import PageLayout

metric_column_names = {'ZT49_D'}


def get_dates_range(engine_df: dict[str, pd.DataFrame]):
    print(engine_df['TAKEOFF']["predicted_y"].dtypes)
    engine_df['TAKEOFF']["predicted_y"].flight_datetime = engine_df['TAKEOFF']["predicted_y"].flight_datetime.astype('datetime64[ns]')
    engine_df['CRUISE']["predicted_y"].flight_datetime = engine_df['CRUISE']["predicted_y"].flight_datetime.astype('datetime64[ns]')
    min_takeoff_ts, max_takeoff_ts = engine_df['TAKEOFF']["predicted_y"]['flight_datetime'].agg(['min', 'max'])
    min_cruise_ts, max_cruise_ts = engine_df['CRUISE']["predicted_y"]['flight_datetime'].agg(['min', 'max'])
    min_ts = min(min_cruise_ts, min_takeoff_ts)
    max_ts = max(max_cruise_ts, max_takeoff_ts)

    return min_ts.to_pydatetime(), max_ts.to_pydatetime()


def engine_flight_date_slider(engine_df: pd.DataFrame):
    date_range = get_dates_range(engine_df)
    
    return st.slider('Date range', value=date_range)


def family_page_info(engine_family_id, family_inference):
    engine_id = st.selectbox(
        'Engine ID',
        tuple(family_inference.keys()),
        key=engine_family_id
    )
    engine_df = family_inference[engine_id]
    date_range = engine_flight_date_slider(engine_df)
    engine_graphics(family_inference[engine_id], date_range)


def slice_df(dataset: pd.DataFrame, ts_range):
    df = dataset
    min_ts, max_ts = ts_range
    filtered_df = df[(df['flight_datetime'] >= min_ts) & (df['flight_datetime'] <= max_ts)]
    return filtered_df


def metric_graphics(metric_name: str, engine_inference, date_range):
    with st.expander(metric_name):
        chartl = get_chart(slice_df(engine_inference['TAKEOFF']["predicted_y"], date_range), metric_name)
        chartr = get_chart(slice_df(engine_inference['CRUISE']["predicted_y"], date_range), metric_name)
        with PageLayout() as page:
            _, left_title_column, _, right_title_column, _ = st.columns([1, 5, 1, 5, 1])
            left_title_column.write("<div style='text-align: center;'>Takeoff</div>", unsafe_allow_html=True)
            right_title_column.write("<div style='text-align: center;'>Cruise</div>", unsafe_allow_html=True)
            page.altair_chart(chartl | chartr, theme="streamlit", use_container_width=True)


def engine_graphics(engine_inference, date_range):
    metric_names = set(engine_inference['TAKEOFF'].columns).difference(['flight_datetime'])

    for metric_name in metric_names:
        metric_graphics(metric_name, engine_inference, date_range)


def family_accordion(engine_family_id: str, family_inference: dict):
    with st.expander(f'Engine family: {engine_family_id}'):
        family_page_info(engine_family_id, family_inference)


def get_chart(dataset: pd.DataFrame, metric_name: str) -> alt.Chart:
    drawing_dataset = (
        dataset[['flight_datetime', metric_name]]
        .astype({'flight_datetime': 'datetime64[ns]'})
    )

    chart = (
        alt.Chart(drawing_dataset)
        .mark_circle()
        .encode(
            x='flight_datetime:T',
            y=f'{metric_name}:Q',
        )
        .interactive()
    )
    return chart
