

from datetime import timedelta
from time import time

import click
import pandas as pd

from biomarkers.tools.control import try_to_run_control_or_exit
from biomarkers.tools.files import export_df
from biomarkers.tools.marker_detection import try_to_load_markers_or_exit
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit


@click.command("control-export")
@click.option("-c", "--control", "fname_control", nargs=1, default="tmp_control.csv", show_default=True, help="Name of the control csv file.")
@click.option("-e", "--export", "fname_export", nargs=1, default="tmp_control.tex", show_default=True, help="Name of the exported file.")
@click.option("-d", "--drop", "columns_text", nargs=1, default="markers_names", show_default=True, help="Comma separated column names to drop.")
@click.option("-g", "--green-only", is_flag=True, default=False, help="Only export rows with 0 red states.")
def control_export(fname_control: str, fname_export: str, columns_text: str, green_only: bool):
    """
    Export a control file.

    biomarkers control-export -c control.json -e control.tex
    """

    columns = try_to_parse_comma_separated_values_or_exit(text=columns_text)
    df = pd.read_csv(fname_control)
    df = df[df["red_states"] == 0] if green_only else df
    df.drop(columns=columns, inplace=True)

    export_df(df=df, fname=fname_export)


@click.command("control-create")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of the markers file.")
@click.option("-c", "--control", "fname_control", nargs=1, default="tmp_control.csv", show_default=True, help="Name of the control csv file.")
@click.option("-l", "--limit", nargs=1, type=int, help="Limits the number of marker sets to consider for control.")
def control_create(fname_markers: str, fname_control: str, limit: int):
    """
    Create a control file.

    biomarkers control-create -m markers.json
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)

    time_start = time()
    df = try_to_run_control_or_exit(markers=markers, limit=limit)
    time_end = time()

    print(f"cpu time: {timedelta(seconds=round(time_end - time_start))}")

    df.to_csv(fname_control, index=False)
    print(f"created {fname_control}")


if __name__ == "__main__":
    """problem = try_to_load_problem_or_exit(fname="../../selvaggio_m1_problem.json")
    markers = try_to_load_markers_or_exit(fname="../../selvaggio_m1_markers.json")
    primes = try_to_load_primes_or_exit(bnet_name="selvaggio_emt")"""

    columns_text = "markers_names"
    fname_control = "../../tmp_control.csv"
    fname_export = "../../tmp_control.tex"

    columns = try_to_parse_comma_separated_values_or_exit(text=columns_text)

    df = pd.read_csv(fname_control)
    df.drop(columns=columns)
    export_df(df=df, fname=fname_export)

