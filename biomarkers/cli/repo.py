

import click

from pyboolnet.repository import get_all_names, get_primes, get_bnet
from pyboolnet.file_exchange import primes2bnet


@click.command("repo")
@click.option("--list", "list_names", is_flag=True, default=False, help="List all networks in repo.")
@click.option("--info", "bnet", nargs=1, help="Show info about a network.")
def repo(list_names: bool, bnet: str):
    """
    Access to the pyboolnet repository.

    biomarkers repo --list
    """

    if list_names:
        print(f"{get_all_names()}")

    if bnet:
        print(get_bnet(name=bnet))





