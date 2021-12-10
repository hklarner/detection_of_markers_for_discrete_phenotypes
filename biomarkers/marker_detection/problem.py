

import logging
from typing import List, Optional, Dict

from pydantic import BaseModel, validator

from biomarkers.mixins import ToJsonMixin

log = logging.getLogger(__name__)


class Problem(BaseModel, ToJsonMixin):
    steady_states: List[List[int]]
    phenotype_indices: List[int]

    phenotype_components: Optional[List[int]]
    phenotype_subspace: Optional[Dict[int, int]]
    primes: Optional[dict]
    component_names: Optional[List[str]]

    def info(self):
        print(f"n_steady_states: {len(self.steady_states)}")
        print(f"component_names: [{','.join(self.component_names)}]")
        print(f"phenotype_components: {self.phenotype_components}")
        print(f"phenotype_subspace: {self.phenotype_subspace}")

    @validator("steady_states")
    def is_binary_vector(cls, v):
        if not set(x for state in v for x in state).issubset({0, 1}):
            raise ValueError(f"steady states must be binary vectors")
        return v


