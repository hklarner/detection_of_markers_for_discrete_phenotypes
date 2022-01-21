

import json
import logging
import sys
from typing import List, Optional

import click
import pandas as pd

COLORS = {int: "white", str: "green", None: "gray", "key": "blue"}

log = logging.getLogger(__name__)


def export_df(df: pd.DataFrame, fname: str, drop_columns: Optional[List[str]] = None) -> Optional[str]:
    if "." not in fname:
        log.error(f"unspecified extension, cannot export data frame: fname={fname}")
        sys.exit(1)

    if df.empty:
        log.error(f"data frame is empty, cannot export data frame: fname={fname}")
        return

    if drop_columns:
        df = df.drop(columns=drop_columns)

    ext = fname.split(".")[1]

    with pd.option_context("display.max_colwidth", 1000):
        if ext == "tex":
            text = df.to_latex(index=False)
        elif ext == "csv":
            text = df.to_csv(index=False)
        elif ext == "md":
            text = df.to_markdown(index=False)
        else:
            log.error(f"unknown extension, cannot export data frame: fname={fname}")
            sys.exit(1)

    with open(fname, "w") as fp:
        fp.write(text)

    log.info(f"created {fname}")

    return text


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
