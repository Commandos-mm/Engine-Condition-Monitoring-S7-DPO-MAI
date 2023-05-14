from typing import TypeAlias, Literal, TypedDict
from collections import defaultdict

import pandas as pd

class EngineDataset(TypedDict):
    predicted_y: pd.DataFrame
    real_y: pd.DataFrame | None


FlightPhase = Literal['CRUISE', 'TAKEOFF']
EngineFamily: TypeAlias = str
EngineId: TypeAlias = str
Inference: TypeAlias = dict[
    EngineFamily, dict[
        EngineId, dict[FlightPhase, EngineDataset]
    ]
]
 
class Pipeline():
    def __init__(self, input, real_y = None) -> None:
        pass
   
    def predict():
        ...
    
    def getformated_data() -> Inference:
        ...

def predict(input: pd.DataFrame) -> Inference:
    """
    Mock function for maintenance characteristics prediction.
    :param input: input DataFrame of aircraft and engine characteristics.
    :return: output groups of DataFrames of predicted maintenance characteristics.
    """
    output: pd.DataFrame = pd.read_csv("src/pipeline/data/y.csv")
    sub_input: pd.DataFrame = input[["engine_id", "flight_datetime", "flight_phase", "engine_family"]]
    df: pd.DataFrame = pd.merge(sub_input, output, on=["engine_id", "flight_datetime", "flight_phase"])
    grouped_output = defaultdict(lambda: defaultdict(dict))
    for (ef, ei, fp), grouped_df in df.groupby(["engine_family", "engine_id", "flight_phase"]):
        grouped_output[ef][ei][fp] = grouped_df
        grouped_output[ef][ei][fp].drop(columns=["engine_family", "engine_id", "flight_phase"],
                                        inplace=True)
    return grouped_output
