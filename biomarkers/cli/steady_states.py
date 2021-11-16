

import click

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.info import echo_steady_state_table


@click.command("steady-states")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("--correlation", nargs=1, help="Marker components to validate, comma separated.")
@click.option("--table", is_flag=True, default=False, help="Displays a steady state table, highlighting constants.")
def steady_states(fname_problem: str, table: bool, correlation: bool):
    """
    Displays information about steady states.

    biomarkers steady-states --constants
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)

    if table:
        echo_steady_state_table(problem=problem)

    if correlation:
        pass



