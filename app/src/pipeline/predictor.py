from typing import TypeAlias, Literal, TypedDict
from collections import defaultdict
from .model import Model

import pandas as pd
import streamlit as st


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
        self.raw_input: pd.DataFrame = input
        self.grouped_input: dict[tuple[str, str], pd.DataFrame] = {
            (ef, fp): df for (ef, fp), df in self.raw_input.groupby(["engine_family", "flight_phase"])
        }
        self.gt: pd.DataFrame = ground_truth
        self.predicted: dict[tuple[str, str], pd.DataFrame] | None = None
        self._preprocess()
        self.model = Model()

    def _preprocess(self):
        for _, df in self.grouped_input.items():
            Pipeline._validate(df)

    @staticmethod
    def _validate(df: pd.DataFrame):
        df.dropna(axis='columns', thresh=20, inplace=True)
        df.dropna(inplace=True)

    def predict(self) -> None:
        self.predicted = self.model.predict(self.grouped_input)

    def get_fmt_data(self) -> Inference:
        sub_input: pd.DataFrame = self.raw_input[[
            "engine_id",
            "flight_datetime",
            "flight_phase",
            "engine_family"
        ]]
        gt_df = None
        if self.gt is not None:
            gt_df = pd.merge(
                sub_input, self.gt, 
                on=["engine_id", "flight_datetime", "flight_phase"]
            )

        grouped_gt = None
        if gt_df is not None:
            grouped_gt = defaultdict(lambda: defaultdict(dict))
            for (ef, ei, fp), ggt in gt_df.groupby(["engine_family", "engine_id", "flight_phase"]):
                grouped_gt[ef][ei][fp] = ggt

        grouped_output = defaultdict(lambda: defaultdict(dict))
        if grouped_gt is not None:
            for (ef, fp), subdf in self.predicted.items():
                for ei, pdf in subdf.groupby("engine_id"):
                    grouped_output[ef][ei][fp] = EngineDataset(
                        predicted_y=pdf,
                        real_y=grouped_gt[ef][ei][fp]
                    )
                    grouped_output[ef][ei][fp]["predicted_y"].drop(
                        columns=["engine_family", "engine_id", "flight_phase"],
                        inplace=True
                    )
                    grouped_output[ef][ei][fp]["real_y"].drop(
                        columns=["engine_family", "engine_id", "flight_phase"],
                        inplace=True
                    )
        else:
            for (ef, fp), subdf in self.predicted.items():
                for ei, pdf in subdf.groupby("engine_id"):
                    grouped_output[ef][ei][fp] = EngineDataset(
                        predicted_y=pdf,
                        real_y=None
                    )
                    grouped_output[ef][ei][fp]["predicted_y"].drop(
                        columns=["engine_family", "engine_id", "flight_phase"],
                        inplace=True
                    )

        return grouped_output
