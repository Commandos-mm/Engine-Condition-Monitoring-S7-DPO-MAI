import altair as alt
import pandas as pd

metric_column_names = {'ZT49_D'}

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