

import click

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.primes import try_to_load_primes_or_exit
from biomarkers.tools.steady_state_correlation import create_steady_state_correlation_graph
from biomarkers.tools.steady_states import echo_steady_state_matrix, compute_steady_state_array


@click.command("steady-state-correlation")
@click.option("-p", "--problem", "fname_problem", nargs=1, help="File name of the problem json to read steady states.")
@click.option("--pdf", "fname_pdf", nargs=1, default="tmp_steady_state_correlation.pdf", show_default=True, help="File name of the correlation graph.")
@click.option("--bnet", "bnet_name", nargs=1, help="File name of bnet file or name in pyboolnet repo to use for computation of steady states.")
@click.option("--tex", "fname_tex", nargs=1, default="tmp_steady_state_correlation_table.tex", show_default=True, help="File name of the correlation table.")
@click.option("--max-steady-states", "max_steady_states", type=int, nargs=1, default=5000, show_default=True, help="Limits number of steady states to compute.")
def steady_state_correlation(fname_problem: str, fname_pdf: str, fname_tex: str, bnet_name: str, max_steady_states: int):
    """
    Computes the blocks of the steady state correlation.

    biomarkers steady-state-correlation -p problem.json --pdf graph.pdf
    """

    if fname_problem:
        problem = try_to_load_problem_or_exit(fname=fname_problem)
        primes = problem.primes
        component_names = problem.component_names
        steady_states = problem.steady_states
    else:
        primes = try_to_load_primes_or_exit(bnet_name=bnet_name)
        component_names = sorted(primes)
        steady_states = compute_steady_state_array(primes=primes, max_steady_states=max_steady_states)

    create_steady_state_correlation_graph(primes=primes, component_names=component_names, steady_states=steady_states, fname_pdf=fname_pdf, fname_tex=fname_tex)


@click.command("steady-state-matrix")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the problem json.")
def steady_state_matrix(fname_problem: str):
    """
    Prints the steady state matrix and highlights values that differ across the steady states.

    biomarkers steady-state-matrix --markers Erk,Mek,Raf
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    echo_steady_state_matrix(problem=problem)



