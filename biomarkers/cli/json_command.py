

import click

from biomarkers.tools.files import read_json_file_and_print_summary
from biomarkers.tools.parsing import try_to_parse_comma_separated_values_or_exit


@click.command("json-info")
@click.argument("fname")
@click.option("--suppress-keys", "suppress_text", default="primes,phenotype_indices,steady_states", show_default=True, help="Suppress keys in summary.")
def json_info(fname: str, suppress_text: str):
    """
    Reads json file and prints summary.

    biomarkers json-info markers.json
    """

    suppress_keys = try_to_parse_comma_separated_values_or_exit(text=suppress_text)
    read_json_file_and_print_summary(fname=fname, suppress_keys=suppress_keys)





