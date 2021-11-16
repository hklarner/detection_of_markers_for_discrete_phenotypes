

import logging
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, validator, root_validator

from biomarkers.mixins import ToJsonMixin

log = logging.getLogger(__name__)


class Problem(BaseModel, ToJsonMixin):
    steady_states: List[List[int]]

    min_marker_size: int = 1
    enable_one_to_one_consistency: bool = True

    component_names: Optional[List[str]]
    max_marker_size: Optional[int]
    phenotype_components: Optional[List[int]]
    phenotype_indices: Optional[List[int]]
    phenotype_subspace: Optional[Dict[str, int]]
    forbidden_marker_components: Optional[List[int]]

    def print_summary(self):
        print(f"n_steady_states: {len(self.steady_states)}")
        print(f"min_marker_size: {self.min_marker_size}")
        print(f"max_marker_size: {self.max_marker_size}")
        print(f"enable_one_to_one_consistency: {self.enable_one_to_one_consistency}")
        print(f"component_names: {self.component_names}")
        print(f"phenotype_components: {self.phenotype_components}")
        print(f"phenotype_subspace: {self.phenotype_subspace}")
        if self.forbidden_marker_components:
            print(f"forbidden_marker_components: {self.forbidden_marker_components} = {[self.component_names[x] for x in self.forbidden_marker_components]}")

    def get_phenotype_indices(self) -> List[int]:
        if self.phenotype_indices:
            return list(self.phenotype_indices)

        phenotypes = []
        phenotype_indices = []
        for state in self.steady_states:
            phenotype = tuple(state[x] for x in self.phenotype_components)
            if phenotype not in phenotypes:
                phenotypes.append(phenotype)
            phenotype_indices.append(phenotypes.index(phenotype))

        self.phenotype_indices = phenotype_indices

        return list(phenotype_indices)

    @validator("steady_states")
    def is_binary_vector(cls, v):
        if not set(x for state in v for x in state).issubset({0, 1}):
            raise ValueError(f"steady states must be binary vectors")
        return v

    @root_validator()
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if len([key for key in ["phenotype_components", "phenotype_indices"] if values.get(key)]) != 1:
            raise ValueError("exactly one of phenotype_components or phenotype_indices must be set")

        if values.get("phenotype_indices"):
            if len(values["phenotype_indices"]) != len(values["steady_states"]):
                raise ValueError("phenotype_indices must be the same length as steady_states")
        return values


if __name__ == "__main__":
    problem = Problem(steady_states=[[1, 0], [0, 0]], phenotype_components=[0, 1])
    x = 1 + 1
