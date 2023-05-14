import streamlit as st
import altair as alt
import pandas as pd
import streamlit_nested_layout

from .page_layout_manager import PageLayout

metric_column_names = {'ZT49_D'}

METRIC_DECRIPTION = {
    'BRAT': 'BLEED RATIO',
    'DEGT': 'EGT DEVIATION FROM BASELINE',
    'DELFN': 'THRUST DERATE',
    'DELN1': 'FAN SPEED DERATE',
    'DELVSV': 'VARIABLE STATOR VANE DEVIATION FROM NOMINAL DPOIL - DELTA OIL PRESSURE',
    'EGTC': 'BASELINE EGT VALUE',
    'EGTHDM': 'EGT MARGIN WITH ADJUSTMENT',
    'EGTHDM_D': 'DVG EGT MARGIN WITH ADJUSTMENT',
    'GEGTMC': 'EGT ETOPS MARGIN (DEG C) CR',
    'GN2MC': 'N2 ETOPS MARGIN (%) CRUISE',
    'GPCN25': 'CORE SPEED DEVIATION FROM BASELINE',
    'GWFM': 'FUEL FLOW DEVIATION FROM BASELINE',
    'PCN12': 'PHYSICAL FAN SPEED (%)',
    'PCN12I': 'INDICATED FAN SPEED (%)',
    'PCN1AR': 'CORRECTED FAN SPEED (%)',
    'PCN1BR': 'CORR FAN SPEED VARIABLE THET',
    'PCN1K': 'CORRECTED FAN SPEED (%)',
    'PCN2C': 'BASELINE CORE SPEED',
    'SLOATL': 'SEA LEVEL OATL',
    'SLOATL_D': 'DVG SEA LEVEL OATL',
    'VSVNOM': 'SCHEDULE VSV POSITION',
    'WBE': 'MEASURED ENGINE BLEED FLOW',
    'WBI': 'ENG BLEED SETTING FOR PEM',
    'WFMP': 'BASELINE FUEL FLOW',
    'ZPCN25_D': 'DVG N2 (HIGH SPEED ROTOR) (%RPM)',
    'ZT49_D': 'DVG EGT-HPT DISCHRG TOT TMP(DEG)',
    'ZTLA_D': 'DVG THROTTLE LEVER ANGLE(DEG)',
    'ZTNAC_D': 'DVG NACELLE TEMP(DEG C)',
    'ZWF36_D': 'DVG FUEL FLOW',
}

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
            if desc := METRIC_DECRIPTION.get(metric_name):
                page.markdown(f"{metric_name} — {desc}")


def engine_graphics(engine_inference, date_range):
    metric_names = set(engine_inference['TAKEOFF']['predicted_y'].columns).difference(['flight_datetime'])

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
