

import click

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.steady_states import echo_steady_state_matrix


@click.command("steady-states-matrix")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the problem json.")
@click.option("--markers", "markers_text", nargs=1, help="Adds marker type to matrix, comma separated names.")
def steady_states_matrix(fname_problem: str, markers_text: str, correlation: bool):
    """
    Prints the steady state matrix.

    biomarkers steady-states-matrix --markers Erk,Mek,Raf
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    echo_steady_state_matrix(problem=problem)



