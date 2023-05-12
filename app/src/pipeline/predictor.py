from typing import TypeAlias, Literal

import pandas as pd

FlightPhase = Literal['CRUISE', 'TAKEOFF']
EngineFamily: TypeAlias = str
 

def predict(input: pd.DataFrame) -> dict[tuple[FlightPhase, EngineFamily], pd.DataFrame]:
    """
    Mock function for maintenance characteristics prediction.
    :param input: input DataFrame of aircraft and engine characteristics.
    :return: output groups of DataFrames of predicted maintenance characteristics.
    """
    output: pd.DataFrame = pd.read_csv("src/pipeline/data/y.csv")
    sub_input: pd.DataFrame = input[["engine_id", "flight_datetime", "flight_phase", "engine_family"]]
    df: pd.DataFrame = pd.merge(sub_input, output, on=["engine_id", "flight_datetime", "flight_phase"])
    phase_df = {k: v for k, v in df.groupby("flight_phase")}
    grouped_output = {
        (phase_key, engine_family_key): df_value
        for phase_key, df in phase_df.items()
        for engine_family_key, df_value in df.groupby("engine_family")
    }
    return grouped_output
