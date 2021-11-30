

from collections import defaultdict
from typing import List, Optional

import click

from biomarkers.marker_detection.problem import Problem


def echo_steady_state_matrix(problem: Problem):
    states = problem.steady_states
    n = len(states[0])
    m = len(states)
    constants = []

    for j in range(n):
        if all(states[x][j] == states[0][j] for x in range(m)):
            constants.append(j)

    for state in states:
        for i, x in enumerate(state):
            click.secho(x, fg="bright_black" if i in constants else None, nl=False)
        click.echo()

    click.echo(" ", nl=False)
    for _ in range(int(n/10)):
        click.echo("         ^", nl=False)
    click.echo()


def print_phenotype_table(steady_states: List[List[int]], phenotype_indices: List[int], phenotype_components: Optional[List[str]] = None):
    states_by_pheno_index = defaultdict(list)

    for ix, iy in enumerate(phenotype_indices):
        states_by_pheno_index[iy].append(steady_states[ix])

    phenotype_by_index = {}
    if phenotype_components:
        for px, states in states_by_pheno_index.items():
            phenotype_by_index[px] = (states[0][x] for x in phenotype_components)

    for px in sorted(states_by_pheno_index):
        print(f"{px: >2} {phenotype_by_index.get(px, '')}: {len(states_by_pheno_index[px])}")
