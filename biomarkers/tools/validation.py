

import logging
import sys
from collections import defaultdict
from typing import List, Optional

from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem

log = logging.getLogger(__name__)


def validate_marker_set_and_print_result(problem: Problem, markers: List[str]):
    marker_indices = [problem.component_names.index(x) for x in markers]
    markertype_to_phenotype = defaultdict(set)

    for i, state in enumerate(problem.steady_states):
        marker_type = tuple(state[x] for x in marker_indices)
        pheno_type = problem.phenotype_indices[i]
        markertype_to_phenotype[marker_type].add(pheno_type)

        if len(markertype_to_phenotype[marker_type]) > 1:
            log.error(f"markers are not consistent with phenotypes: {dict(markertype_to_phenotype)}, state_index={i}")
            sys.exit(1)

    log.info(f"markers are consistent with phenotypes.")


def assert_consistency_of_component_names_or_exit(primes: Optional[dict] = None, markers: Optional[Markers] = None, problem: Optional[Problem] = None):
    names_primes = set(primes) or set()
    names_markers = set(markers.component_names) if markers else set()
    names_problem = set(problem.component_names) if problem else set()

    if names_primes:
        diff = names_markers.difference(names_primes)
        if diff:
            print(f"names of markers do not belong to primes: difference={diff}")
            sys.exit(1)

        diff = names_problem.difference(names_primes)
        if diff:
            print(f"names of problem do not belong to primes: difference={diff}")
            sys.exit(1)

    else:
        if names_problem:
            diff = names_markers.difference(names_problem)
            if diff:
                print(f"names of markers do not belong to problem: difference={diff}")
                sys.exit(1)
