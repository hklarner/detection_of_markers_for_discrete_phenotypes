

from typing import List

from biomarkers.marker_detection.problem import Problem


def compute_type_indices(states: List[List[int]], components: List[int]) -> List[int]:
    type_indices = []
    types = []

    for state in states:
        type_ = (state[x] for x in components)
        if type_ not in types:
            types.append(type_)

        type_indices = types.index(type_)

    return type_indices


def validate(problem: Problem, marker_family: List[List[int]]) -> List[str]:
    markers = marker_family[0]
    marker_type_indices = compute_type_indices(states=problem.steady_states, components=markers)
    phenotype_indices = compute_type_indices(states=problem.steady_states, components=problem.phenotype_components) if problem.phenotype_components else problem.phenotype_indices



