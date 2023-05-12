import pandas as pd
from typing import Dict, Tuple, Set, Callable


def grouper(input: Dict[Tuple[str, ...],pd.DataFrame],
            keys: Tuple[str, ...]) -> Dict[Tuple[str, ...], pd.DataFrame]:
    """
    Helper function for recursive grouping dict of pandas DataFrames.
    """
    if not keys:
        return input

    to_tuple_transformer: Callable = lambda element: element if isinstance(element, tuple) else (element, )

    grouped_df: Dict[Tuple[str, ...], pd.DataFrame] = {
        (next_key, *to_tuple_transformer(curr_key)): next_df
        for curr_key, curr_df in input.items()
        for next_key, next_df in curr_df.groupby(keys[-1])
    }

    return grouper(grouped_df, keys[:-1])


def predict(input: pd.DataFrame,
            keys: Tuple[str, ...] = ("engine_family", "flight_phase")) -> Dict[Tuple[str, ...], pd.DataFrame]:
    """
    Mock function for maintenance characteristics prediction.
    :param input: input DataFrame of aircraft and engine characteristics.
    :param keys: keys that are used for grouping output data.
    :return: output groups of DataFrames of predicted maintenance characteristics.
    """
    # TODO: add model prediction instead of valid data
    output: pd.DataFrame = pd.read_csv("src/pipeline/data/y.csv")
    sub_input_keys: Set[str, ...] = {"engine_id", "flight_datetime", "flight_phase", *keys}
    sub_input: pd.DataFrame = input[list(sub_input_keys)]
    df: pd.DataFrame = pd.merge(sub_input, output, on=["engine_id", "flight_datetime", "flight_phase"])
    phase_df: Dict = {k: v for k, v in df.groupby(keys[-1])}

    return grouper(phase_df, keys[:-1])
