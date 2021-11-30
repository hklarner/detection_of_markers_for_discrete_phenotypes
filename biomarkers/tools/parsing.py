

import logging
import sys
from typing import List, Optional

log = logging.getLogger(__name__)


def assert_exclusive_arguments_or_exit(**kwargs):
    if len([value for key, value in kwargs.items() if value]) > 1:
        log.error(f"exactly one of the arguments must be given: {list(kwargs.items())}")
        sys.exit(1)


def try_to_parse_comma_separated_values_or_exit(text: str) -> Optional[List[str]]:
    try:
        return text.split(",")
    except ValueError as error:
        log.error(f"cannot parse components: text={text}, error={error}")
        sys.exit()


def try_to_parse_comma_separated_items_or_exit(text: str) -> Optional[dict]:
    try:
        return parse_comma_separated_items(text=text, value_map=int)
    except ValueError as error:
        log.error(f"cannot parse subspace: text={text}, error={error}")
        sys.exit()


def parse_comma_separated_items(text: str, value_map: callable = lambda x: x) -> dict:
    d = {}
    for item in text.split(","):
        key, value = item.split("=")
        d[key] = value_map(value)
    return d


if __name__ == "__main__":
    d = try_to_parse_comma_separated_items_or_exit(text="k=2,t=1")
    print(d)
    pass
