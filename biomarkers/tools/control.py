

import logging
import sys

from pyboolnet.prime_implicants import create_constants
from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem
from biomarkers.pyboolnet_extensions import percolate_and_find_new_constants
from biomarkers.tools.phenotypes import get_steady_state_representative
from biomarkers.tools.phenotypes import get_subspace

log = logging.getLogger(__name__)


def try_to_run_control_or_exit(problem: Problem, markers: Markers, primes: dict, phenotype_index: int):
    if not problem.has_phenotype_index(index=phenotype_index):
        log.error(f"can not run control, phenotype index does not exist: phenotype_index={phenotype_index}, set(problem.phenotype_indices)={set(problem.phenotype_indices)}")
        sys.exit(1)

    representative_state = get_steady_state_representative(problem=problem, phenotype_index=phenotype_index)
    desired_phenotype = get_subspace(state=representative_state, components=list(problem.phenotype_subspace))

    for marker_components in markers.indices:
        marker_type = get_subspace(state=representative_state, components=marker_components, names=problem.component_names)
        new_primes = create_constants(primes=primes, constants=marker_type, copy=True)
        new_steady_states = compute_steady_states(primes=new_primes, max_output=5000)
        new_constants = {problem.component_names.index(k): v for k, v in percolate_and_find_new_constants(primes=new_primes).items()}
        marker_type = get_subspace(state=representative_state, components=marker_components)

        print(f"marker_components={marker_components}")
        print(f"marker_type={marker_type}")
        print(f"desired_phenotype={desired_phenotype}")
        print(f"representative_state={representative_state}")
        print(f"len(new_steady_states)={len(new_steady_states)}")
        print(f"new_constants={new_constants}")
        break

