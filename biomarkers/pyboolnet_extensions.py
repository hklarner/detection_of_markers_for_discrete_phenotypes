

from typing import Dict, Optional

import networkx
from pyboolnet.interaction_graphs import primes2igraph, igraph2image
from pyboolnet.prime_implicants import find_constants
from pyboolnet.prime_implicants import percolate


def create_percolated_igraph(primes: dict, fname: Optional[str] = None) -> networkx.DiGraph:
    igraph = primes2igraph(primes=primes)
    primes_new = percolate(primes=primes, copy=True)
    igraph_new = primes2igraph(primes=primes_new)

    edges = set(igraph.edges)
    edges_new = set(igraph_new.edges)

    for e in edges.difference(edges_new):
        igraph.edges[e]["color"] = "0.6 0.5 1.0"

    if fname:
        igraph2image(igraph=igraph, fname_image=fname, layout_engine="dot")

    return igraph_new


def add_style_cascades(igraph: networkx.DiGraph, penwidth: int = 5, color: str = "black"):
    """
    Increases the pen width of edges whose targets are of in-degree one.

    **arguments**:
        * *igraph*: interaction graph
        * *penwidth*: pen width of cascade edges

    **example**::

          >>> add_style_cascades(igraph)
    """

    for source, target in igraph.edges():
        if source == target:
            continue
        if igraph.in_degree(target) == 1:
            igraph[source][target]["penwidth"] = penwidth
            igraph[source][target]["color"] = color

            igraph.nodes[source]["penwidth"] = penwidth
            igraph.nodes[source]["color"] = "black"

            igraph.nodes[target]["penwidth"] = penwidth
            igraph.nodes[target]["color"] = "black"


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
    from pyboolnet.prime_implicants import create_constants

    primes = get_primes(name="selvaggio_emt")

    create_percolated_igraph(primes=create_constants(primes=primes, constants={"RAF1": 1}, copy=True), fname="junk.pdf")


