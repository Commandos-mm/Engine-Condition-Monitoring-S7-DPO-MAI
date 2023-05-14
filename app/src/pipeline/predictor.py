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


class Pipeline:
    def __init__(self, input: pd.DataFrame, ground_truth: pd.DataFrame = None) -> None:
        self.input: pd.DataFrame = input
        self.gt: pd.DataFrame = ground_truth
        self.predicted: pd.DataFrame | None = None
   
    def predict(self) -> None:
        self.predicted: pd.DataFrame = pd.read_csv("src/pipeline/data/y.csv")
    
    def get_fmt_data(self) -> Inference:
        sub_input: pd.DataFrame = self.input[["engine_id", "flight_datetime", "flight_phase", "engine_family"]]
        predicted_df: pd.DataFrame = pd.merge(sub_input, self.predicted,
                                              on=["engine_id", "flight_datetime", "flight_phase"])
        gt_df: pd.DataFrame = self.gt and pd.merge(sub_input, self.gt,
                                                   on=["engine_id", "flight_datetime", "flight_phase"])

        grouped_output = defaultdict(lambda: defaultdict(dict))
        if gt_df:
            for (ef, ei, fp), (pgdf, gtdf) in zip(predicted_df.groupby(["engine_family", "engine_id", "flight_phase"]),
                                                  gt_df.groupby(["engine_family", "engine_id", "flight_phase"])):
                grouped_output[ef][ei][fp] = EngineDataset(predicted_y=pgdf, real_y=gtdf)
                grouped_output[ef][ei][fp]["predicted_y"].drop(columns=["engine_family", "engine_id", "flight_phase"],
                                                               inplace=True)
                grouped_output[ef][ei][fp]["real_y"].drop(columns=["engine_family", "engine_id", "flight_phase"],
                                                          inplace=True)
        else:
            for (ef, ei, fp), pgdf in predicted_df.groupby(["engine_family", "engine_id", "flight_phase"]):
                grouped_output[ef][ei][fp] = EngineDataset(predicted_y=pgdf, real_y=None)
                grouped_output[ef][ei][fp]["predicted_y"].drop(columns=["engine_family", "engine_id", "flight_phase"],
                                                               inplace=True)
        return grouped_output
