

import json
from typing import List

import click

COLORS = {int: "white", str: "green", None: "gray", "key": "blue"}


def read_json_file_and_print_summary(fname: str, suppress_keys: List[str]):
    with open(fname, "r") as fp:
        data = json.load(fp)

    echo_json(data=data, spaces_current=0, spaces_inc=2, suppress_keys=suppress_keys)


def echo_json(data, spaces_current: int, spaces_inc: int, suppress_keys: List[str]):
    s = spaces_current * " "
    n = spaces_inc * " "
    d = type(data)

    if d is dict:
        click.secho(s + "{")

        for key, value in data.items():
            v = type(value)

            click.secho(s + n + f'"{key}"', fg=COLORS["key"], nl=False)
            click.secho(': ', nl=False)

            if key in suppress_keys:
                click.secho("<suppressed>,")
                continue

            if v in [str, int, None]:
                click.secho(value, fg=COLORS[v], nl=False)
                click.secho(",")

            else:
                echo_json(data=value, spaces_current=spaces_current + spaces_inc, spaces_inc=spaces_inc, suppress_keys=suppress_keys)

        click.secho(s + "}")

    elif d is list:
        if not data:
            click.secho(f"{data},")

        elif type(data[0]) in [int, str]:
            click.secho(f"{data},")

        else:
            click.secho(f"[{data[0]}, ..], ({len(data)})")

    elif data is None or d is bool:
        click.secho(f"{data},")

    else:
        print(f"unknown type: type={d}, data={data}")


if __name__ == "__main__":
    read_json_file_and_print_summary(fname="../../selvaggio_markers.json", suppress_keys=["primes", "phenotype_indices", "steady_states"])
