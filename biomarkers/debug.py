
from pyboolnet.repository import get_primes
from pyboolnet.trap_spaces import compute_steady_states

from biomarkers.factories.markers import markers_from_problem
from biomarkers.marker_detection.options import Options
from biomarkers.marker_detection.problem import Problem

if __name__ == "__main__":
    primes = get_primes(name="selvaggio_emt")
    phenotype_subspace = {"AJ_b1": 0, "AJ_b2": 0, "FA_b1": 1, "FA_b2": 0, "FA_b3": 0}

    names = sorted(primes)
    steady_states_indices = [list(map(int, x)) for x in compute_steady_states(primes=primes, max_output=5000, representation="str")]
    phenotype_subspace_indices = {names.index(k): v for k, v in phenotype_subspace.items()}
    phenotype_indices = [1 if all(x[k] == v for k, v in phenotype_subspace_indices.items()) else 0 for x in steady_states_indices]

    problem = Problem(
        steady_states=steady_states_indices,
        component_names=names, phenotype_indices=phenotype_indices,
        phenotype_subspace=phenotype_subspace_indices)

    options = Options(enable_one_to_one=False, marker_size_max=3, forbidden=[names.index(k) for k in phenotype_subspace])
    markers = markers_from_problem(problem=problem, options=options, dry=False)

    print(len(markers.indices))

