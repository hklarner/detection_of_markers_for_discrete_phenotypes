

from typing import List, Optional
from collections import defaultdict

import click

from biomarkers.marker_detection.problem import Problem
from biomarkers.answer_set_programming.model import Model


def echo_steady_state_table(problem: Problem):
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


def print_phenotype_marker_comparison(steady_states: List[List[int]], phenotype_indices: List[int]):
    pass


def print_asp_program(model: Model):
    for line in model.program:
        if len(line) < 200:
            print(line.replace("%", "\n%"))
        else:
            print(f"{line[:50]} ... (len(line)={len(line)})")


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
