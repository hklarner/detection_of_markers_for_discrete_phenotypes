

from typing import Dict

from pyboolnet.prime_implicants import find_constants
from pyboolnet.prime_implicants import percolate


def percolate_and_find_new_constants(primes: dict) -> Dict[str, int]:
    constants = find_constants(primes=primes)
    new_constants = find_constants(primes=percolate(primes=primes, copy=True))
    difference = {k: new_constants[k] for k in new_constants if k not in constants}

    return difference
