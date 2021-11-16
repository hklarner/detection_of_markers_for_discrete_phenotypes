

from datetime import timedelta
from time import time

import click

from biomarkers.factories.model import model_from_problem
from biomarkers.tools.debugger import debug_by_relaxation
from biomarkers.tools.info import print_phenotype_table
from biomarkers.tools.marker_detection import try_to_create_marker_detection_problem_or_exit
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_items_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit
from biomarkers.tools.primes import try_to_load_primes_or_exit


@click.command("problem-solve-heuristic")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", help="File name of the marker detection problem.")
@click.option("--save-markers", "fname_marker_family", nargs=1, help="File name to save makers, json or csv.")
def problem_solve_heuristic(fname_problem: str, fname_marker_family: str):
    """
    Solves a marker detection problem using a brute force approach.
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)

    time_start = time()
    markers = 0
    time_end = time()

    print(f"cpu time: {timedelta(milliseconds=time_end - time_start)}")
    print(markers)


@click.command("problem-solve")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("-m", "--markers", "fname_markers", default="markers.json", show_default=True, nargs=1, help="Saves the markers as json or csv.")
def problem_solve(fname_problem: str, fname_markers: str):
    """
    Solves a marker detection problem.
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    model = model_from_problem(problem=problem)

    time_start = time()
    markers = model.solve()
    markers.component_names = problem.component_names
    time_end = time()
    model.print_solve_result()

    print(f"first three marker sets: {markers.indices[:3]}")
    print(f"cpu time: {timedelta(seconds=time_end - time_start)}")
    print(f"{len(markers)=}")

    if fname_markers:
        markers.to_json(fname=fname_markers)


@click.command("problem-debug")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("--assumption", nargs=1, help="The debugging assumption.")
def problem_debug(fname_problem: str, assumption: str):
    """
    Debugs a marker detection problem.
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    debug_by_relaxation(model=model_from_problem(problem=problem), assumption=assumption)


@click.command("problem-create")
@click.option("-p", "--problem", "fname_output", nargs=1, default="problem.json", show_default=True, help="Name of the marker detection problem json file.")
@click.option("--bnet", "bnet_name", nargs=1, help="File name of bnet file or name in pyboolnet repo.")
@click.option("--exact", is_flag=True, default=False, help="Enables 1-to-1 consistency between marker types and phenotypes.")
@click.option("--phenotype", "phenotype_text", required=True, nargs=1, help="Phenotype definition by subspace or components, comma-separated.")
@click.option("--forbidden", "forbidden_text", nargs=1, help="Components that are not allowed as markers, comma-separated.")
@click.option("--max-markers", "max_marker_size", type=int, nargs=1, help="Limits the maximal size of a marker set.")
@click.option("--max-steady-states", "max_steady_states", type=int, nargs=1, default=5000, show_default=True, help="Limits number of steady states to compute.")
def problem_create(fname_output: str, bnet_name: str, phenotype_text: str, forbidden_text: str, max_steady_states: int, exact: bool, max_marker_size: int):
    """
    Creates a marker detection problem.

    biomarkers create --bnet selvaggio-emt --phenotype AJ_b1=0,AJ_b2=0,FA_b1=1,FA_b2=0,FA_b3=0
    """

    primes = try_to_load_primes_or_exit(bnet_name=bnet_name)
    phenotype_components = try_to_parse_comma_separated_values_or_exit(text=phenotype_text) if "=" not in phenotype_text else None
    phenotype_subspace = try_to_parse_comma_separated_items_or_exit(text=phenotype_text) if "=" in phenotype_text else None
    forbidden = try_to_parse_comma_separated_values_or_exit(text=forbidden_text) if forbidden_text else None
    problem = try_to_create_marker_detection_problem_or_exit(
        primes=primes, phenotype_components=phenotype_components, phenotype_subspace=phenotype_subspace, max_steady_states=max_steady_states, forbidden=forbidden)

    problem.enable_one_to_one_consistency = exact
    problem.max_marker_size = max_marker_size
    problem.to_json(fname=fname_output)
    problem.print_summary()
    print_phenotype_table(steady_states=problem.steady_states, phenotype_indices=problem.get_phenotype_indices())



