

import os.path
import sys
import logging

from pyboolnet.file_exchange import bnet2primes
from pyboolnet.repository import get_primes, get_all_names


log = logging.getLogger(__name__)


def try_to_load_primes_or_exit(bnet_name: str) -> dict:
    if os.path.isfile(bnet_name):
        try:
            return bnet2primes(bnet=bnet_name)
        except Exception as error:
            log.error(f"could not load primes: {bnet_name=}, {error=}")
            sys.exit(1)

    if bnet_name in get_all_names():
        return get_primes(name=bnet_name)

    log.error(f"bnet name is not a file and not in pyboolnet repo: {bnet_name=}")
    sys.exit(1)

