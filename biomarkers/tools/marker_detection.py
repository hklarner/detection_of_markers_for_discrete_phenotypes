

import json
import logging
import sys
from typing import List

from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.factories.problem import phenotype_indices_from_subspace, phenotype_indices_from_components
from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem

log = logging.getLogger(__name__)


def try_to_create_marker_detection_problem_or_exit(primes: dict, phenotype_components: List[str], phenotype_subspace: dict, max_steady_states: int) -> Problem:
    names = sorted(primes)
    steady_states = [[int(x[k]) for k in names] for x in compute_steady_states(primes=primes, max_output=max_steady_states)]

    try:
        if phenotype_subspace:
            phenotype_subspace = {names.index(x): phenotype_subspace[x] for x in phenotype_subspace}
            phenotype_indices = phenotype_indices_from_subspace(steady_states=steady_states, phenotype_subspace=phenotype_subspace)
            problem = Problem(primes=primes, component_names=names, steady_states=steady_states, phenotype_indices=phenotype_indices, phenotype_subspace=phenotype_subspace)
        else:
            phenotype_components = [names.index(x) for x in phenotype_components]
            phenotype_indices = phenotype_indices_from_components(steady_states=steady_states, phenotype_components=phenotype_components)
            problem = Problem(primes=primes, component_names=names, steady_states=steady_states, phenotype_components=phenotype_components, phenotype_indices=phenotype_indices)

    except Exception as error:
        log.error(f"failed to create marker detection problem: error={error}")
        sys.exit(1)

    return problem


def try_to_load_problem_or_exit(fname: str) -> Problem:
    try:
        with open(fname, "r") as fp:
            return Problem(**json.load(fp))
    except Exception as error:
        log.error(f"could not load marker detection problem: error={error}")
        sys.exit(1)


def try_to_load_markers_or_exit(fname: str) -> Markers:
    try:
        with open(fname, "r") as fp:
            return Markers(**json.load(fp))
    except Exception as error:
        log.error(f"could not load markers: error={error}")
        sys.exit(1)


if __name__ == '__main__':
    problem = Problem(steady_states=[[0]], phenotype_indices=[1], enable_one_to_one_consistency=False)
    problem = try_to_load_problem_or_exit("../../marker_problem.json")
    pass
