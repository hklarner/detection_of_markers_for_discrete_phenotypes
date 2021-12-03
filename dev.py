from pyboolnet.repository import get_primes
from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.marker_detection.problem import Problem
from biomarkers.factories.markers import markers_from_problem
from pyboolnet.repository import get_primes
from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.factories.markers import markers_from_problem
from biomarkers.marker_detection.problem import Problem

if __name__ == "__main__":
    primes = get_primes(name="selvaggio_emt")
    phenotype_subspace = {"AJ_b1": 0, "AJ_b2": 0, "FA_b1": 1, "FA_b2": 0, "FA_b3": 0}

    names = sorted(primes)
    steady_states_indices = [list(map(int, x)) for x in compute_steady_states(primes=primes, max_output=5000, representation="str")]
    phenotype_subspace_indices = {names.index(k): v for k, v in phenotype_subspace.items()}
    phenotype_indices = [1 if all(x[k] == v for k, v in phenotype_subspace_indices.items()) else 0 for x in steady_states_indices]

    problem = Problem(
        steady_states=steady_states_indices, enable_one_to_one_consistency=False,
        component_names=names, max_marker_size=3, phenotype_indices=phenotype_indices,
        phenotype_subspace=phenotype_subspace_indices, forbidden_marker_components=[names.index(k) for k in phenotype_subspace])

    markers = markers_from_problem(problem=problem)

    print(len(markers.indices))
