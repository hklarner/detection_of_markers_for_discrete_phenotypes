

import logging
from functools import lru_cache
from typing import List

import pandas as pd
from pydantic import BaseModel

from biomarkers.marker_detection.options import Options
from biomarkers.marker_detection.problem import Problem
from biomarkers.mixins import ToJsonMixin

log = logging.getLogger(__name__)


class Markers(BaseModel, ToJsonMixin):
    indices: List[List[int]]
    problem: Problem
    options: Options

    def __len__(self) -> int:
        return len(self.indices)

    @property
    @lru_cache()
    def indices_named(self) -> List[List[str]]:
        return [[self.problem.component_names[x] for x in indices] for indices in self.indices]

    @property
    @lru_cache()
    def unique_indices(self) -> List[int]:
        return sorted(set(x for markers in self.indices for x in markers))

    def info(self):
        if len(self.indices) > 3:
            print(f"len(markers.indices)={len(self.indices)}")
            print(f"markers.indices[:3]={self.indices[:3]}")
        else:
            print(f"markers.indices={self.indices}")

    def to_csv(self, fname: str) -> pd.DataFrame:
        df = self.to_df()
        df.to_csv(fname, index=False)

        log.info(f"created csv file: fname={fname}")

        return df

    def to_df(self) -> pd.DataFrame:
        data = {self.problem.component_names[x]: [] for x in self.unique_indices}

        for indices in self.indices_named:
            for name in data:
                data[name].append(1 if name in indices else 0)

        return pd.DataFrame(data=data)

    class Config:
        keep_untouched = (property,)
