

import click

from biomarkers.tools.graphs import create_marker_frequency_graph
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit, try_to_load_markers_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit
from biomarkers.tools.validation import validate_marker_set_and_print_result


@click.command("markers-graph")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of markers file.")
@click.option("-g", "--graph", "fname_graph", nargs=1, default="tmp_markers_graph.pdf", show_default=True, help="Name of markers graph file.")
def markers_graph(fname_markers: str, fname_graph: str):
    """
    Creates a marker graph.

    biomarkers markers-graph -m markers.json -g markers_graph.pdf
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    create_marker_frequency_graph(markers=markers, fname=fname_graph)


@click.command("markers-info")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of markers file.")
def markers_info(fname_markers: str):
    """
    Prints info about a markers file.

    biomarkers markers-info -m markers.json
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    markers.info()
    markers.problem.info()


@click.command("markers-export")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of markers file.")
@click.option("--csv", "fname_csv", nargs=1, default="markers.csv", show_default=True, help="Name of csv file.")
@click.option("--header", "enable_header", is_flag=True, default=False, show_default=True, nargs=1, help="If header is enabled, all rows consist of 0 / 1 values.")
def markers_export(fname_markers: str, fname_csv: str, enable_header: bool):
    """
    Exports markers as CSV.

    biomarkers markers-export -m markers.csv
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    #markers.to_csv(fname=fname_csv, enable_header=enable_header)
    print(markers.to_df())


@click.command("markers-validate")
@click.option("--markers", "markers_text", nargs=1, help="Marker components to validate, comma separated.")
def markers_validate(fname_problem: str, markers_text: str):
    """
    Validates a marker set.

    biomarkers markers-validate -m RAP1,ERK,p120_AJ
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    markers = try_to_parse_comma_separated_values_or_exit(text=markers_text)
    validate_marker_set_and_print_result(problem=problem, markers=markers)


@click.command("markers-factorize")
@click.option("-m", "--markers", "markers_text", nargs=1, help="Marker components to validate, comma separated.")
def markers_factorize(fname_problem: str, markers_text: str):
    """
    Factorizes a marker set.

    biomarkers markers-factorize -m RAP1,ERK,p120_AJ
    """

    pass



