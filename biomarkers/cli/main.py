

import logging
import sys

import click
import pandas as pd

from biomarkers import read_version_txt
from biomarkers.cli.control import control_create, control_export
from biomarkers.cli.json_command import json_info
from biomarkers.cli.markers import markers_factorize, markers_validate, markers_export, markers_info, markers_count
from biomarkers.cli.problem import problem_create, problem_info, problem_solve
from biomarkers.cli.repo import repo
from biomarkers.cli.steady_states import steady_state_matrix, steady_state_correlation

log = logging.getLogger()
logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO, force=True)
logging.getLogger("pyboolnet").setLevel(logging.ERROR)


@click.group(chain=True, context_settings=dict(help_option_names=["-h", "--help"]), invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, default=False, type=bool, help="Display version.")
@click.option("--debug", is_flag=True, default=False, type=bool, help="Set log level to debug.")
@click.pass_context
def main(ctx, version: bool, debug: bool):
    if debug:
        logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG, force=True)

    if version:
        click.echo(f"version: {read_version_txt()}")
        click.echo(f"python-version: {sys.version_info}")

    if ctx.invoked_subcommand is None and len(sys.argv) == 1:
        click.echo(main.get_help(ctx))

    pd.options.display.float_format = "{:.2f}".format


main.add_command(problem_solve)
main.add_command(problem_create)
main.add_command(repo)
main.add_command(markers_validate)
main.add_command(markers_export)
main.add_command(markers_info)
main.add_command(markers_count)
main.add_command(problem_info)
main.add_command(markers_factorize)
main.add_command(steady_state_matrix)
main.add_command(steady_state_correlation)
main.add_command(control_create)
main.add_command(control_export)
main.add_command(json_info)
