

import click

from biomarkers.graphs.marker_count import create_marker_count_graph, get_component_counts_from_markers
from biomarkers.graphs.marker_factorization import create_marker_factorization_graphs_by_size
from biomarkers.tools.factorization import factorize_marker_sets
from biomarkers.tools.files import export_df
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit, try_to_load_markers_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit
from biomarkers.tools.validation import validate_marker_set_and_print_result


@click.command("markers-count")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="The name of the markers file.")
@click.option("--pdf", "fname_pdf", nargs=1, default="tmp_markers_count.pdf", show_default=True, help="Creates a pdf of the interaction graph with marker counts.")
@click.option("--tex", "fname_tex", nargs=1, default="tmp_markers_count.tex", show_default=True, help="Creates a tex of the markers count table.")
def markers_count(fname_markers: str, fname_pdf: str, fname_tex: str):
    """
    Counts how often components appear in the marker sets.
    Prints a summary table.

    biomarkers markers-count -m markers.json --pdf markers_count.pdf
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    component_counts = get_component_counts_from_markers(markers=markers)
    print(component_counts.to_string(index=False))
    create_marker_count_graph(markers=markers, component_counts=component_counts, fname_pdf=fname_pdf)

    if fname_tex:
        export_df(df=component_counts, fname=fname_tex)


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
@click.option("--pdf", "fname_pdf_base", nargs=1, help="Name of pdf file for visualizing the factorization.")
def markers_factorize(fname_markers: str, fname_tex: str, fname_pdf_base: str):
    """
    Factorizes a marker set.

    A factorization is a non-unique representation of a set of markers as a product of marker subsets, see http://dl.acm.org/doi/10.1145/3486713.3486729 for details.
    The command divides the marker sets into sets of identical cardinality and heuristically searches for a factorization with as many and as large as possible factors.
    Two types of factors may occur:

        * singleton factors, e.g. S(1,2) \n
        * long factors, e.g. L(n=2,k=8)

    A singleton factor S(1,2) indicates that every marker set contains either component 1 or component 2.
    A long factor L(n=2,k=8) indicates that every marker set contains an additional pair of components (n=2) and that there are 8 pairs to choose from (k=8).
    If k<=3 then the markers subsets are explicitly enumerated, e.g. {{25,14},{39,31}} means that every marker set contains either the pair {25,14} or the pair {39,31} of components.

    The command prints a table of data with columns

        * n_components: the number of components in each marker set \n
        * n_markers: the number of marker sets \n
        * factorization: the factorization of the set \n
        * n_factors_used: the number of factors used in the factorization \n
        * n_factors_available: the numer of factors detected in the heuristic search

    Example:

    $ biomarkers markers-factorize -m markers.json
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)
    optimal_factors_by_size = factorize_marker_sets(markers=markers, fname_tex=fname_tex)
    create_marker_factorization_graphs_by_size(markers=markers, optimal_factorizations_by_size=optimal_factors_by_size, fname_pdf_base=fname_pdf_base)
