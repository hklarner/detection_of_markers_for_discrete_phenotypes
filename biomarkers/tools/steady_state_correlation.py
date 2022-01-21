

import logging
from collections import defaultdict
from itertools import combinations
from typing import List
from typing import Optional

import pandas as pd
from networkx import DiGraph
from pyboolnet.interaction_graphs import igraph2image, primes2igraph

log = logging.getLogger(__name__)


def create_steady_state_correlation_graph(primes: dict, component_names: List[str], steady_states: List[List[int]], fname_pdf: Optional[str] = None, fname_tex: Optional[str] = None) -> DiGraph:
    igraph = primes2igraph(primes=primes)
    correlated_components = [[component_names[x] for x in block] for block in compute_correlated_components(steady_states=steady_states)]

    if len(correlated_components) > 19:
        log.warning(f"number of blocks exceeds maximum number of colors, colors will repeat: n_blocks={len(correlated_components)}, n_colors=19")

    igraph.graph["edge"]["color"] = "gray"

    for x in igraph.nodes:
        igraph.nodes[x]["fillcolor"] = None

    for i, block in enumerate(correlated_components):
        for x in block:
            igraph.nodes[x]["fillcolor"] = f"/pastel19/{i + 1}"
            igraph.nodes[x]["color"] = "black"

    for block in correlated_components:
        sub_graph = igraph.subgraph(nodes=block)
        for n in sub_graph.nodes:
            if sub_graph.in_degree(n) == 0:
                igraph.nodes[n]["penwidth"] = 5

    if fname_pdf:
        igraph2image(igraph=igraph, fname_image=fname_pdf, layout_engine="dot")
        log.info(f"created {fname_pdf}")

    if fname_tex:
        tex = pd.DataFrame(data={"correlation blocks": [', '.join(x) for x in correlated_components]}).to_latex()
        with open(fname_tex, "w") as fp:
            fp.write(tex)

        log.info(f"created {fname_tex}")

    return igraph


def compute_correlated_components(steady_states: List[List[int]]) -> List[List[int]]:
    pairs = list(combinations(iterable=range(len(steady_states[0])), r=2))
    first_link = {}

    s = steady_states[0]
    for u, v in pairs:
        first_link[(u, v)] = s[u] == s[v]

    for s in steady_states[1:]:
        if not pairs:
            break

        for u, v in list(pairs):
            current_link = s[u] == s[v]

            if first_link[(u, v)] != current_link:
                pairs.remove((u, v))

    seen = set()
    linked_components = defaultdict(set)
    for a, b in pairs:
        if a in seen:
            continue

        linked_components[a].add(a)
        linked_components[a].add(b)
        seen.add(b)

    linked_components = [list(x) for x in linked_components.values()]

    return linked_components
