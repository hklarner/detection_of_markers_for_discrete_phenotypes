

import click

from biomarkers.tools.control import try_to_run_control_or_exit
from biomarkers.tools.marker_detection import try_to_load_markers_or_exit, try_to_load_problem_or_exit
from biomarkers.tools.primes import try_to_load_primes_or_exit


@click.command("control-create")
@click.option("-m", "--markers", "fname_markers", nargs=1, default="tmp_markers.json", show_default=True, help="Name of the markers file.")
@click.option("-c", "--control", "fname_control", nargs=1, default="tmp_control.json", show_default=True, help="Name of the control summary file.")
def control_create(fname_markers: str, fname_control: str):
    """
    Create a control file.

    biomarkers control-create -m markers.json
    """

    markers = try_to_load_markers_or_exit(fname=fname_markers)

    df = try_to_run_control_or_exit(markers=markers)

    if fname_control:
        df.to_csv(fname_control)


if __name__ == "__main__":
    problem = try_to_load_problem_or_exit(fname="../../selvaggio_m1_problem.json")
    markers = try_to_load_markers_or_exit(fname="../../selvaggio_m1_markers.json")
    primes = try_to_load_primes_or_exit(bnet_name="selvaggio_emt")

    control_summary = try_to_run_control_or_exit(problem=problem, markers=markers, primes=primes)

