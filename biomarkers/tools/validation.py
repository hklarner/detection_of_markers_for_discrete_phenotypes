

import logging
import sys
from collections import defaultdict
from typing import List

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
