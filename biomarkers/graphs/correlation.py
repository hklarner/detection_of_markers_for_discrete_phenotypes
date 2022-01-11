

import logging
from typing import Optional

import pandas as pd
from networkx import DiGraph
from pyboolnet.interaction_graphs import igraph2image, primes2igraph

from biomarkers.marker_detection.problem import Problem
from biomarkers.steady_states.correlation import compute_correlated_components

log = logging.getLogger(__name__)


def create_steady_state_correlation_graph(problem: Problem, fname_pdf: Optional[str] = None, fname_tex: Optional[str] = None) -> DiGraph:
    igraph = primes2igraph(primes=problem.primes)
    correlated_components = [[problem.component_names[x] for x in block] for block in compute_correlated_components(steady_states=problem.steady_states)]

    if len(correlated_components) > 19:
        log.warning(f"number of blocks of correlated exceeds maximum number of color, colors will repeat: {len(correlated_components)=}, n_colors=19")

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
