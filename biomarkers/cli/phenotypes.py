

import click

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.steady_states import print_phenotype_table


@click.command("phenotypes")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("--correlation", nargs=1, help="Marker components to validate, comma separated.")
@click.option("--table", is_flag=True, default=False, help="Displays a steady state table, highlighting constants.")
def phenotypes(fname_problem: str, table: bool, correlation: bool):
    """
    Displays information about phenotypes.

    biomarkers phenotypes -h
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)

    if phenotypes:
        print_phenotype_table(steady_states=problem.steady_states, phenotype_indices=problem.phenotype_indices)







