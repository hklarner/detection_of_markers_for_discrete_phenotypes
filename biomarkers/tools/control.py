

import logging
import sys
from collections import defaultdict
from typing import List, Dict, Callable

import pandas as pd
from pyboolnet.prime_implicants import create_constants
from pyboolnet.trap_spaces import steady_states as compute_steady_states

from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem
from biomarkers.pyboolnet_extensions import percolate_and_find_new_constants, is_trap_space

log = logging.getLogger(__name__)


def try_to_run_control_or_exit(problem: Problem, markers: Markers, primes: dict) -> pd.DataFrame:
    if not problem.phenotype_subspace:
        log.error("control requires a phenotype subspace, try a different problem file.")
        sys.exit(1)

    desired_subspaces = [problem.phenotype_subspace]
    desired_steady_states = filter_states_by_containment_in_subspaces(states=problem.steady_states, subspaces=desired_subspaces)
    data = defaultdict(list)

    for marker_components in markers.indices:
        marker_types = find_projections(states=desired_steady_states, components=marker_components)

        for marker_type in marker_types:
            constants = {problem.component_names[x]: y for x, y in zip(marker_components, marker_type)}
            new_primes = create_constants(primes=primes, constants=constants, copy=True)

            new_steady_states = [list(map(int, x)) for x in compute_steady_states(primes=new_primes, max_output=5000, representation="str")]
            red_states, green_states = [], []

            for state in new_steady_states:
                if any(all(state[x] == subspace[x] for x in subspace) for subspace in desired_subspaces):
                    green_states.append(state)
                else:
                    red_states.append(state)

            percolated_constants = percolate_and_find_new_constants(primes=new_primes)

            data["markers"].append(marker_components)
            data["markers_names"].append([problem.component_names[x] for x in marker_components])
            data["control"].append(marker_type)
            data["green_states"].append(len(green_states))
            data["red_states"].append(len(red_states))
            data["n_percolation"].append(len(percolated_constants))
            data["percolated_phenotype"].append(any(all(problem.component_names[x] in percolated_constants for x in subspace) for subspace in desired_subspaces))
            data["is_trap_space"].append(is_trap_space(primes=primes, subspace={problem.component_names[k]: v for k, v in zip(marker_components, marker_type)}))

    df = pd.DataFrame(data=data)
    print(df)

    return df


def filter_states_by_containment_in_subspaces(states: List[List[int]], subspaces: List[Dict[int, int]], quantifier: Callable = any) -> List[List[int]]:
    return [state for state in states if quantifier(all(state[x] == subspace[x] for x in subspace) for subspace in subspaces)]


def filter_subspaces_by_containment_of_state(state: List[int], subspaces: List[Dict[int, int]]) -> List[Dict[int, int]]:
    return [subspace for subspace in subspaces if all(state[x] == subspace[x] for x in subspace)]


def find_projections(states: List[List[int]], components: List[int]) -> List[List[int]]:
    projections = []

    for state in states:
        projection = [state[component] for component in components]
        if projection not in projections:
            projections.append(projection)

    return projections


if __name__ == "__main__":
    df = pd.read_csv("../../selvaggio_m1_control.json", index_col=[0])
    #print(df[df["red_states"] == 0][["markers", "control", "red_states", "percolated_phenotype"]].to_latex(index=False))
    print(df[df["is_trap_space"] == False])

    #print(df.loc[df["red_states"] == 0])
    #print(df.query('red_states == 0'))
