

import click

from biomarkers.factories.program import program_from_problem
from biomarkers.tools.marker_detection import try_to_load_problem_or_exit


@click.command("asp-export")
@click.option("-p", "--problem", "fname_problem", nargs=1, default="problem.json", show_default=True, help="File name of the marker detection problem.")
@click.option("--program", "fname_asp", nargs=1, default="program.asp", show_default=True, help="Name of asp file.")
def asp_export(fname_problem: str, fname_asp: str):
    """
    Exports or prints asp program.

    biomarkers asp-export
    """

    problem = try_to_load_problem_or_exit(fname=fname_problem)

    if fname_asp:
        model = program_from_problem(problem=problem)
        model.to_asp(fname=fname_asp)



