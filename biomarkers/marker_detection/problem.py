

import logging
from typing import List, Optional, Dict

from pydantic import BaseModel, validator

from biomarkers.mixins import ToJsonMixin

log = logging.getLogger(__name__)


class Problem(BaseModel, ToJsonMixin):
    steady_states: List[List[int]]
    phenotype_indices: List[int]

    phenotype_components: Optional[List[int]] = None
    phenotype_subspace: Optional[Dict[int, int]] = None
    primes: Optional[dict] = None
    component_names: Optional[List[str]] = None

    def info(self):
        print(f"n_steady_states: {len(self.steady_states)}")
        if self.component_names:
            components = sorted(self.phenotype_components if self.phenotype_components else self.phenotype_subspace)
            mapping = {i: self.component_names[i] for i in components}
            print(f"component_names: {mapping}")

        if self.phenotype_components:
            print(f"phenotype_components: {self.phenotype_components}")
        else:
            print(f"phenotype_subspace: {self.phenotype_subspace}")

    def get_phenotype_text(self, phenotype_index: int) -> str:
        for i, state in enumerate(self.steady_states):
            if self.phenotype_indices[i] == phenotype_index:
                if self.phenotype_components:
                    phenotype = {x: state[x] for x in self.phenotype_components}
                    text = f"{phenotype}"
                elif phenotype_index == 1:
                    phenotype = self.phenotype_subspace
                    text = f"{phenotype}"
                else:
                    phenotype = self.phenotype_subspace
                    text = f"not {phenotype}"
                return text

        raise ValueError(f"unknown phenotype index: {phenotype_index=}")

    @validator("steady_states")
    def is_binary_vector(cls, v):
        if not set(x for state in v for x in state).issubset({0, 1}):
            raise ValueError(f"steady states must be binary vectors")
        return v


if __name__ == '__main__':
    problem = Problem(steady_states=[], phenotype_indices=[])
    print(problem)

