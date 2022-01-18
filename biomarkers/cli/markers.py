

import click

from biomarkers.graphs.marker_frequency import create_marker_frequency_graph
from biomarkers.tools.factorization import factorize_marker_sets
from biomarkers.tools.files import export_df
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
@click.option("--csv", "fname_csv", nargs=1, default="tmp_markers.csv", show_default=True, help="Name of csv file.")
def markers_export(fname_markers: str, fname_csv: str):
    """
    Exports markers as CSV.

    biomarkers markers-export -m markers.csv
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    df = markers.to_csv(fname=fname_csv)
    print(df)


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
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of markers file.")
@click.option("--tex", "fname_tex", nargs=1, help="Name of tex file for factorization.")
def markers_factorize(fname_markers: str, fname_tex: str):
    """
    Factorizes a marker set.

    A factorization is a non-unique representation of a set of markers as a product of marker subsets, see http://dl.acm.org/doi/10.1145/3486713.3486729 for details.
    The command divides the marker sets into sets of identical cardinality and heuristically searches for a factorization with as many and as large as possible factors.
    Two types of factors may occur:

        * singleton factors, e.g. S(1,2) \n
        * long factors, e.g. L(n=2,k=8)

    A singleton factor S(1,2) indicates that every marker set contains either component 1 or component 2.
    A long factor L(n=2,k=8) indicates that every marker set contains an additional pair of components (n=2) and that their are 8 pairs to choose from (k=8).
    If k<=3 then the markers subsets are explicitely enumerated, e.g. {{25,14},{39,31}} means that every markers set contains either the pair {25,14} or the pair {39,31} of components.

    The command prints a table of data with columns

        * n_components: the number of components in each marker set \n
        * n_markers: the number of marker sets \n
        * factorization: the factorization of the set \n
        * n_factorization: the number of factors used in the factorization \n
        * n_factors: the numer of factors detected in the heuristic search

    Example:

    $ biomarkers markers-factorize -m markers.json
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    df = factorize_marker_sets(markers=markers)
    print(df.to_string(index=False))

    if fname_tex:
        export_df(df=df, fname=fname_tex)





