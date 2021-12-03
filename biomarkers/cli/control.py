

import click

from biomarkers.tools.control import try_to_run_control_or_exit
from biomarkers.tools.marker_detection import try_to_load_markers_or_exit, try_to_load_problem_or_exit
from biomarkers.tools.primes import try_to_load_primes_or_exit


@click.command("control-create")
@click.argument("bnet", nargs=1)
@click.option("-p", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("-m", "fname_markers", nargs=1, default="markers.json", show_default=True, help="Name of the markers file.")
@click.option("-c", "fname_control", nargs=1, default="control_summary.json", show_default=True, help="Name of the control summary file.")
def control_create(fname_markers: str, fname_problem: str, fname_control: str, bnet: str):
    """
    Create a control file.

    BNET: File name of bnet file or name in pyboolnet repo.

    biomarkers control-create -m markers.json selvaggio_emt
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)
    markers = try_to_load_markers_or_exit(fname=fname_markers)
    primes = try_to_load_primes_or_exit(bnet_name=bnet)

    df = try_to_run_control_or_exit(problem=problem, markers=markers, primes=primes)

    if fname_control:
        df.to_csv(fname_control)


if __name__ == "__main__":
    problem = try_to_load_problem_or_exit(fname="../../selvaggio_m1_problem.json")
    markers = try_to_load_markers_or_exit(fname="../../selvaggio_m1_markers.json")
    primes = try_to_load_primes_or_exit(bnet_name="selvaggio_emt")

    control_summary = try_to_run_control_or_exit(problem=problem, markers=markers, primes=primes)

