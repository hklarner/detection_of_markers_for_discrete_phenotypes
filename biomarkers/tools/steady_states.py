

from collections import defaultdict

import click
import pandas as pd

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
        click.echo("─────────┴", nl=False)
    click.echo()


def print_phenotype_table(problem: Problem):
    counts = defaultdict(int)
    for phenotype_index in problem.phenotype_indices:
        counts[phenotype_index] += 1

    data = defaultdict(list)
    for phenotype_index, count in sorted(counts.items()):
        data["phenotype_index"].append(phenotype_index)
        data["phenotype_text"].append(problem.get_phenotype_text(phenotype_index=phenotype_index))
        data["n_steady_states"].append(count)

    print(pd.DataFrame(data=data))

