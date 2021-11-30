

import logging
import sys

import click
import pandas as pd

from biomarkers import read_version_txt
from biomarkers.cli.control import control_create
from biomarkers.cli.markers import markers_factorize, markers_validate, markers_export, markers_info
from biomarkers.cli.phenotypes import phenotypes
from biomarkers.cli.problem import problem_create, problem_debug
from biomarkers.cli.problem import problem_solve, problem_solve_heuristic
from biomarkers.cli.repo import repo
from biomarkers.cli.steady_states import steady_states_matrix

log = logging.getLogger()
logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
logging.getLogger("pyboolnet").setLevel(logging.ERROR)


@click.group(chain=True, context_settings=dict(help_option_names=["-h", "--help"]), invoke_without_command=True)
@click.pass_context
def main(ctx):
    click.echo(f"version: {read_version_txt()}")

    if ctx.invoked_subcommand is None and len(sys.argv) == 1:
        click.echo(main.get_help(ctx))

    pd.options.display.float_format = "{:.2f}".format


main.add_command(problem_solve)
main.add_command(problem_solve_heuristic)
main.add_command(problem_create)
main.add_command(repo)
main.add_command(markers_validate)
main.add_command(markers_export)
main.add_command(markers_info)
main.add_command(problem_debug)
main.add_command(markers_factorize)
main.add_command(steady_states_matrix)
main.add_command(phenotypes)
main.add_command(control_create)
