

import json
import logging
import sys
from typing import List

from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.marker_detection.problem import Problem
from biomarkers.marker_detection.markers import Markers

log = logging.getLogger(__name__)


def try_to_create_marker_detection_problem_or_exit(primes: dict, forbidden: List[str], phenotype_components: List[str], phenotype_subspace: dict, max_steady_states: int) -> Problem:
    names = sorted(primes)
    steady_states = compute_steady_states(primes=primes, max_output=max_steady_states)
    steady_state_indices = [[int(x[k]) for k in names] for x in steady_states]

    try:
        if phenotype_components:
            problem = Problem(
                component_names=names, steady_states=steady_state_indices, phenotype_components=[names.index(x) for x in phenotype_components])
        else:
            phenotype_indices = [1 if all(x[k] == phenotype_subspace[k] for k in phenotype_subspace) else 0 for x in steady_states]
            problem = Problem(component_names=names, steady_states=steady_state_indices, phenotype_indices=phenotype_indices, phenotype_subspace=phenotype_subspace)
        if forbidden:
            problem.forbidden_marker_components = [names.index(x) for x in forbidden]

    except Exception as error:
        log.error(f"failed to create marker detection problem: {error=}")
        sys.exit(1)

    return problem


def solve_marker_detection_problem(problem: Problem) -> List[int]:
    return []


def try_to_load_problem_or_exit(fname: str) -> Problem:
    try:
        with open(fname, "r") as fp:
            return Problem(**json.load(fp))
    except Exception as error:
        log.error(f"could not load marker detection problem: {error=}")
        sys.exit(1)


def try_to_load_markers_or_exit(fname: str) -> Markers:
    try:
        with open(fname, "r") as fp:
            return Markers(**json.load(fp))
    except Exception as error:
        log.error(f"could not load markers: {error=}")
        sys.exit(1)


if __name__ == '__main__':
    problem = Problem(steady_states=[[0]], phenotype_indices=[1], enable_one_to_one_consistency=False)
    problem = try_to_load_problem_or_exit("../../marker_problem.json")
    pass
