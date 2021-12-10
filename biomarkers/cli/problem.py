

from datetime import timedelta
from time import time

import click

from biomarkers.factories.markers import markers_from_problem
from biomarkers.factories.program import program_from_problem
from biomarkers.marker_detection.options import Options
from biomarkers.tools.marker_detection import try_to_create_marker_detection_problem_or_exit
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit
from biomarkers.tools.parsing import indexify_names_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_items_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit
from biomarkers.tools.primes import try_to_load_primes_or_exit
from biomarkers.tools.steady_states import print_phenotype_table


@click.command("problem-solve")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="tmp_problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("-m", "--markers", "fname_markers", default="tmp_markers.json", show_default=True, nargs=1, help="Saves the markers as json or csv.")
@click.option("--enable-one-to-one", is_flag=True, default=False, help="Enables 1-to-1 consistency between marker types and phenotypes.")
@click.option("--forbidden", "forbidden_text", nargs=1, help="Components that are not allowed as markers, comma-separated.")
@click.option("--marker-size-max", "marker_size_max", type=int, nargs=1, help="Limits the maximal size of a marker set.")
@click.option("--dry", is_flag=True, default=False, help="Prints ASP program and stops.")
def problem_solve(fname_problem: str, fname_markers: str, enable_one_to_one: bool, forbidden_text: str, marker_size_max: int, dry: bool):
    """
    Solves a marker detection problem.
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    forbidden_names = try_to_parse_comma_separated_values_or_exit(text=forbidden_text) if forbidden_text else None
    forbidden = indexify_names_or_exit(names=problem.component_names, subset=forbidden_names)
    options = Options(forbidden=forbidden, enable_one_to_one=enable_one_to_one, marker_size_max=marker_size_max)

    time_start = time()
    markers = markers_from_problem(problem=problem, options=options, dry=dry)
    time_end = time()

    print(f"cpu time: {timedelta(seconds=time_end - time_start)}")
    markers.info()

    if fname_markers:
        markers.to_json(fname=fname_markers)


@click.command("problem-create")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="tmp_problem.json", show_default=True, help="Name of the marker detection problem json file.")
@click.option("--bnet", "bnet_name", nargs=1, help="File name of bnet file or name in pyboolnet repo.")
@click.option("--max-steady-states", "max_steady_states", type=int, nargs=1, default=5000, show_default=True, help="Limits number of steady states to compute.")
@click.option("--phenotype", "phenotype_text", required=True, nargs=1, help="Phenotype definition by subspace or components, comma-separated.")
def problem_create(fname_problem: str, bnet_name: str, phenotype_text: str, max_steady_states: int):
    """
    Creates a marker detection problem.

    biomarkers problem-create --bnet selvaggio-emt --phenotype AJ_b1=0,AJ_b2=0,FA_b1=1,FA_b2=0,FA_b3=0
    """

    primes = try_to_load_primes_or_exit(bnet_name=bnet_name)
    phenotype_components = try_to_parse_comma_separated_values_or_exit(text=phenotype_text) if "=" not in phenotype_text else None
    phenotype_subspace = try_to_parse_comma_separated_items_or_exit(text=phenotype_text) if "=" in phenotype_text else None

    problem = try_to_create_marker_detection_problem_or_exit(
        primes=primes, phenotype_components=phenotype_components, phenotype_subspace=phenotype_subspace,
        max_steady_states=max_steady_states)

    problem.to_json(fname=fname_problem)
    problem.info()

    print_phenotype_table(problem=problem)


@click.command("problem-info")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="Name of the marker detection problem json file.")
@click.option("--asp", "print_asp", is_flag=True, default=False, help="Print ASP program.")
@click.option("--enable-one-to-one", is_flag=True, default=False, help="Enables 1-to-1 consistency between marker types and phenotypes.")
def problem_info(fname_problem: str, print_asp: bool, enable_one_to_one: bool):
    """
    Displays info about a problem file.

    biomarkers problem-info --problem selvaggio_problem.json
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    problem.info()
    print_phenotype_table(problem=problem)

    if print_asp:
        program = program_from_problem(problem=problem, options=Options(enable_one_to_one=enable_one_to_one))
        print(program)


if __name__ == "__main__":
    fname_problem = "../../selvaggio_problem.json"
    problem = try_to_load_problem_or_exit(fname=fname_problem)

    time_start = time()
    markers = markers_from_problem(problem=problem)
    time_end = time()

    print(f"first three marker sets: {markers.indices[:3]}")
    print(f"cpu time: {timedelta(seconds=time_end - time_start)}")
    print(f"len(markers)={len(markers.indices)}")

