

import logging
import sys
from collections import defaultdict
from typing import List, Dict, Callable

import click
import pandas as pd
from pyboolnet.prime_implicants import percolate, find_constants
from pyboolnet.trap_spaces import compute_steady_states

from biomarkers.marker_detection.markers import Markers
from biomarkers.pyboolnet_extensions import is_trap_space

log = logging.getLogger(__name__)


def try_to_run_control_or_exit(markers: Markers, limit: int) -> pd.DataFrame:
    if not markers.problem.phenotype_subspace:
        log.error("control requires a phenotype subspace, try a different problem file.")
        sys.exit(1)

    component_names = markers.problem.component_names
    primes = markers.problem.primes

    desired_subspaces = [markers.problem.phenotype_subspace]
    desired_steady_states = filter_states_by_containment_in_subspaces(states=markers.problem.steady_states, subspaces=desired_subspaces)
    data = defaultdict(list)
    scenarios = markers.indices[:limit] if limit else markers.indices

    with click.progressbar(scenarios, label="Checking each marker set for control strategies") as markers_indices:

        for indices in markers_indices:
            marker_types = find_projections(states=desired_steady_states, components=indices)

            for marker_type in marker_types:
                constants = {component_names[x]: y for x, y in zip(indices, marker_type)}
                primes_new = percolate(primes=primes, add_constants=constants, copy=True)
                constants_percolated = {k: v for k, v in find_constants(primes=primes_new).items() if k not in constants}
                steady_states_new = [list(map(int, x)) for x in compute_steady_states(primes=primes_new, max_output=5000, representation="str")]

                red_states, green_states = [], []
                for state in steady_states_new:
                    if any(all(state[x] == subspace[x] for x in subspace) for subspace in desired_subspaces):
                        green_states.append(state)
                    else:
                        red_states.append(state)

                data["markers"].append(indices)
                data["markers_names"].append([component_names[x] for x in indices])
                data["control"].append(marker_type)
                data["green_states"].append(len(green_states))
                data["red_states"].append(len(red_states))
                data["n_percolation"].append(len(constants_percolated))
                data["percolated_phenotype"].append(any(all(component_names[x] in constants_percolated for x in subspace) for subspace in desired_subspaces))
                data["is_trap_space"].append(is_trap_space(primes=primes, subspace={component_names[k]: v for k, v in zip(indices, marker_type)}))

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
