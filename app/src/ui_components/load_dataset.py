from .page_layout_manager import PageLayout

import pandas as pd


def read_csv(path: str):
    return pd.read_csv(path).astype({'flight_datetime': 'datetime64[ns]'})


def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    with PageLayout() as page:
        uploaded_files = page.file_uploader("Choose a X.csv and y.csv", accept_multiple_files=True)
        x, y = None, None
        for file in uploaded_files: 
            if file.name == 'X.csv':
                x = pd.read_csv(file).astype({'flight_datetime': 'datetime64[ns]'})
            else:
                y = pd.read_csv(file).astype({'flight_datetime': 'datetime64[ns]'})
        return x, y

    