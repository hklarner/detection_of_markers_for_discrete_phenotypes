

import click

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit, try_to_load_markers_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit
from biomarkers.tools.validation import validate_marker_set_and_print_result


@click.command("markers-export")
@click.option("--markers", "fname_markers", nargs=1, default="markers.json", show_default=True, help="Name of markers file.")
@click.option("--csv", "fname_csv", nargs=1, default="markers.csv", show_default=True, help="Name of csv file.")
@click.option("--header", "enable_header", is_flag=True, default=False, show_default=True, nargs=1, help="If header is enabled, all rows consist of 0 / 1 values.")
def markers_export(fname_markers: str, fname_csv: str, enable_header: bool):
    """
    Exports a marker set.

    biomarkers markers-export markers.csv
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    markers.to_csv(fname=fname_csv, enable_header=enable_header)


@click.command("markers-validate")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("-m", "--markers", "markers_text", nargs=1, help="Marker components to validate, comma separated.")
def markers_validate(fname_problem: str, markers_text: str):
    """
    Validates a marker set.

    biomarkers markers-validate -m RAP1,ERK,p120_AJ
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    markers = try_to_parse_comma_separated_values_or_exit(text=markers_text)
    validate_marker_set_and_print_result(problem=problem, markers=markers)


@click.command("markers-factorize")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("-m", "--markers", "markers_text", nargs=1, help="Marker components to validate, comma separated.")
def markers_factorize(fname_problem: str, markers_text: str):
    """
    Factorizes a marker set.

    biomarkers markers-factorize -m RAP1,ERK,p120_AJ
    """

    pass



