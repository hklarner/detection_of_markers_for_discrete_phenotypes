

from typing import Dict, List, Union, Optional

from biomarkers.marker_detection.problem import Problem


def get_subspace(state: List[int], components: List[int], names: Optional[List[str]] = None) -> Dict[Union[int, str], int]:
    names = names or {x: x for x in components}
    return {names[x]: state[x] for x in components}


def get_phenotype_subspace(problem: Problem, phenotype_index: int) -> Dict[str, int]:
    steady_state = get_steady_state_representative(problem=problem, phenotype_index=phenotype_index)


def get_steady_state_representative(problem: Problem, phenotype_index: int) -> List[int]:
    for state, index in zip(problem.steady_states, problem.phenotype_indices):
        if index == phenotype_index:
            return state

