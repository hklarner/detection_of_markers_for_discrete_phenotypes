

import logging
from functools import cached_property
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

    @cached_property
    def indices_named(self) -> List[List[str]]:
        return [[self.problem.component_names[x] for x in indices] for indices in self.indices]

    @cached_property
    def unique_indices(self) -> List[int]:
        return sorted(set(x for markers in self.indices for x in markers))

    def info(self):
        if len(self.indices) > 3:
            print(f"len(markers.indices)={len(self.indices)}")
            print(f"markers.indices[:3]={self.indices[:3]}")
        else:
            print(f"markers.indices={self.indices}")

    def to_csv(self, fname: str, enable_header: bool = False):
        if enable_header:
            if self.problem:
                lines = [[self.problem.component_names[x] for x in self.unique_indices]]
                lines += [[self.problem.component_names[x] for x in markers] for markers in self.indices]
            else:
                lines = [str(x) for x in self.unique_indices]
                lines += [[str(x) for x in markers] for markers in self.indices]
        else:
            if self.problem:
                lines = [[self.problem.component_names[x] for x in markers] for markers in self.indices]
            else:
                lines = [[str(x) for x in markers] for markers in self.indices]

        with open(fname, "w") as fp:
            fp.write('\n'.join(', '.join(line) for line in lines))

        log.info(f"created csv file: fname={fname}")

    def to_df(self) -> pd.DataFrame:
        data = {name: [] for name in sorted(self.unique_indices)}
        for indices in self.indices_named:
            for name in data:
                data[name].apppend(1 if name in indices else 0)

        return pd.DataFrame(data=data)

    class Config:
        keep_untouched = (cached_property,)
