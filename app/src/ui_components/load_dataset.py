from .page_layout_manager import PageLayout

import pandas as pd


def read_csv(path: str):
    return pd.read_csv(path).astype({'flight_datetime': 'datetime64[ns]'})


def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    with PageLayout() as page:
        uploaded_file = page.file_uploader("Choose a file")
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file.getvalue()), None
        else:

            return read_csv('src/pipeline/data/X.csv'), read_csv('src/pipeline/data/y.csv')
    