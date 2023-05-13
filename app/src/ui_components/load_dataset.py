from .page_layout_manager import PageLayout

import pandas as pd


def load_dataset() -> pd.DataFrame:
    with PageLayout() as page:
        uploaded_file = page.file_uploader("Choose a file")
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file.getvalue())
        else:

            return pd.read_csv('src/pipeline/data/X.csv')
    