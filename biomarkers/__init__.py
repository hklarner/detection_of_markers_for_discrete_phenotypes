

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT, "version.txt")


def read_version_txt() -> str:
    with open(PATH, "r") as fp:
        return fp.readline()


def write_version_txt(version: str):
    with open(PATH, "w") as fp:
        fp.write(version)
