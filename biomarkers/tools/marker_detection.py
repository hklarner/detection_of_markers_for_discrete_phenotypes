

import json
import logging
import sys
from typing import List
from typing import Optional

from biomarkers.factories.problem import phenotype_indices_from_subspace, phenotype_indices_from_components
from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem
from biomarkers.tools.steady_states import compute_steady_state_array

log = logging.getLogger(__name__)


def try_to_create_marker_detection_problem_or_exit(
        primes: dict,
        phenotype_components: Optional[List[str]],
        phenotype_subspace: Optional[dict],
        max_steady_states: int,
) -> Problem:
    names = sorted(primes)
    steady_states = compute_steady_state_array(primes=primes, max_steady_states=max_steady_states)

    if phenotype_subspace:
        phenotype_components = None
        phenotype_subspace = {names.index(x): phenotype_subspace[x] for x in phenotype_subspace}
        phenotype_indices = phenotype_indices_from_subspace(
            steady_states=steady_states,
            phenotype_subspace=phenotype_subspace,
        )
    elif phenotype_components:
        phenotype_subspace = None
        phenotype_components = [names.index(x) for x in phenotype_components]
        phenotype_indices = phenotype_indices_from_components(
            steady_states=steady_states,
            phenotype_components=phenotype_components,
        )
    else:
        log.error(f"either phenotype subspace or phenotype components must be specified: {phenotype_subspace=}, {phenotype_components=}")
        sys.exit(1)

    try:
        problem = Problem(
            primes=primes,
            component_names=names,
            steady_states=steady_states,
            phenotype_indices=phenotype_indices,
            phenotype_components=phenotype_components,
            phenotype_subspace=phenotype_subspace,
        )
    except Exception as error:
        log.error(f"failed to create marker detection problem: {error=}")
        sys.exit(1)

    return problem


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



