

import click

from biomarkers.graphs.correlation import create_steady_state_correlation_graph
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.steady_states import echo_steady_state_matrix


@click.command("steady-states-correlation")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="tmp_problem.json", show_default=True, help="File name of the problem json.")
@click.option("-g", "--graph", "fname_graph", nargs=1, default="tmp_steady_state_correlation_graph.pdf", show_default=True, help="File name of the correlation graph.")
@click.option("--tex", "fname_tex", nargs=1, default="tmp_steady_state_correlation_table.tex", show_default=True, help="File name of the correlation table.")
def steady_state_correlation(fname_problem: str, fname_graph: str, fname_tex: str):
    """
    Creates the steady state correlation graph.

    biomarkers steady-state-correlation -p problem.json -g graph.pdf
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    create_steady_state_correlation_graph(problem=problem, fname_pdf=fname_graph, fname_tex=fname_tex)


@click.command("steady-states-matrix")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the problem json.")
@click.option("-m", "--markers", "markers_text", nargs=1, help="Adds marker type to matrix, comma separated names.")
def steady_states_matrix(fname_problem: str, markers_text: str, correlation: bool):
    """
    Prints the steady state matrix.

    biomarkers steady-states-matrix --markers Erk,Mek,Raf
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    echo_steady_state_matrix(problem=problem)



