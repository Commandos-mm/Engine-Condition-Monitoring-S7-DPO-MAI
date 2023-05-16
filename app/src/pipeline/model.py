import pickle
import os

import pandas as pd

from collections import defaultdict
from typing import TypedDict


class Model:
    ENGINE_FAMILIES: list = ["CF34-8E", "CFM56-5B", "CFM56-7"]

    class ModelKey(TypedDict):
        engine_family: str
        flight_phase: str
        metric: str

    def __init__(self, path_to_models: str = "src/pipeline/models"):
        self.models = defaultdict(lambda: defaultdict(dict))
        for filename in os.listdir(path_to_models):
            full_filename = os.path.join(path_to_models, filename)
            if os.path.isfile(full_filename):
                key_tuple: Model.ModelKey = Model._get_key_by_filename(filename)
                with open(full_filename, "rb") as model_file:
                    self.models[key_tuple["engine_family"]][key_tuple["flight_phase"]][key_tuple["metric"]] = pickle.load(model_file)

    def predict(self, input: dict[tuple[str, str], pd.DataFrame]) -> dict[tuple[str, str], pd.DataFrame]:
        output = dict()
        for (ef, fp), X in input.items():
            if not (ef in self.models.keys() and fp in self.models[ef].keys()):
                continue
            # TODO: remove lately, datetime shouldn't be str
            X = X.astype({'flight_datetime': 'str'})
            info_df: pd.DataFrame = X[[
                "engine_id",
                "flight_datetime",
                "flight_phase",
                "engine_family"
            ]]
            for metric, model in self.models[ef][fp].items():
                predicted = model.predict(X)
                metric_df = pd.DataFrame({metric: predicted})
                info_df = info_df.reset_index(drop=True).join(metric_df.reset_index(drop=True), how='left')
            # TODO: remove lately, datetime shouldn't be str
            info_df = info_df.astype({'flight_datetime': 'datetime64[ns]'})
            output[(ef, fp)] = info_df

        return output

    @staticmethod
    def _get_key_by_filename(filename: str) -> ModelKey:
        flight_phase: str = "TAKEOFF" if filename[1] == "t" else "CRUISE"
        matches: list = [ef for ef in Model.ENGINE_FAMILIES if ef.lower().endswith(filename[2:4])]
        if not matches:
            raise Exception("Model error in pickle format. Couldn't find engine family")
        engine_family: str = matches[0]
        metric: str = filename[5:-4]
        return Model.ModelKey(engine_family=engine_family,
                              flight_phase=flight_phase,
                              metric=metric)
