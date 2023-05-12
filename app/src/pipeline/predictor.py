import pandas as pd


def predict(_input: pd.DataFrame) -> pd.DataFrame:
    """
    Mock function for maintenance characteristics prediction.
    :param _input: input DataFrame of aircraft and engine characteristics.
    :return: output DataFrame of predicted maintenance characteristics.
    """
    return pd.read_csv("src/pipeline/data/y.csv")
