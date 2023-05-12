from typing import TypeAlias

# import streamlit as st
import pandas as pd

import pipeline


# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     ts = pd.read_csv(uploaded_file.getvalue())
# else:
#     idx = pd.date_range("2018-01-01", periods=5, freq="H")
#     ts = pd.Series(range(len(idx)), index=idx)


# st.line_chart(ts)

ts = ''
engine_inference_mapping = pipeline.predict(ts)


for family_id, inference in engine_inference_mapping.items():
    for metric_name in set(inference.columns).difference(['timestamp', 'n1_modifier']):
        metric_df = inference[['timestamp', 'flight_phase', metric_name]]
        
        drawing_dataset = pd.DataFrame(
            {
                'timestamp': metric_df['timestamp'],
                'cruise': metric_df[metric_df['flight_phase'] == 'CRUISE'],
                'takeoff': metric_df[metric_df['flight_phase'] =='TAKEOFF'],
            }
        )
        print(drawing_dataset)
        exit()
        st.line_chart(drawing_dataset)



