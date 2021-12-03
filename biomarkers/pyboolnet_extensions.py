

from typing import Dict

from pyboolnet.prime_implicants import find_constants
from pyboolnet.prime_implicants import percolate


def percolate_and_find_new_constants(primes: dict) -> Dict[str, int]:
    old_constants = find_constants(primes=primes)
    constants = find_constants(primes=percolate(primes=primes, copy=True))
    new_constants = {k: constants[k] for k in constants if k not in old_constants}

    return new_constants


def is_trap_space(primes: dict, subspace: Dict[str, int]) -> bool:
    """
    Tests whether *subspace* is a trap space in *primes*.

    **arguments**:
        * *primes*: prime implicants
        * *subspace*: a subspace

    **returns**:
        * *result: whether *subspace* is a trap space

    **example**::

        >>> is_trap_space(primes=primes, subspace={'RAF':1, 'ERK':0, 'MEK':1})
        True
    """

    subspace_items = set(subspace.items())
    for name, value in subspace_items:
        if not any(set(p.items()).issubset(subspace_items) for p in primes[name][value]):
            return False

    return True


if __name__ == "__main__":
    from pyboolnet.repository import get_primes
    from pyboolnet.trap_spaces import trap_spaces as compute_trap_spaces

    primes = get_primes(name="selvaggio_emt")
    trap_spaces = compute_trap_spaces(primes=primes)

    for trap_space in trap_spaces:
        for k in trap_space:
            break
        trap_space[k] = 1 - trap_space[k]
        print(is_trap_space(primes=primes, subspace=trap_space))


