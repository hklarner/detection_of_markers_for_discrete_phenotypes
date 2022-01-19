

import logging
from typing import Optional, Dict, List

from networkx import DiGraph
from pyboolnet.interaction_graphs import igraph2image, primes2igraph

from biomarkers.marker_detection.markers import Markers
from biomarkers.tools.integer_sets import IntegerSets

log = logging.getLogger(__name__)


def create_marker_factorization_graphs_by_size(markers: Markers, optimal_factorizations_by_size: Dict[int, List[IntegerSets]], fname_pdf_base: Optional[str] = None) -> Dict[int, DiGraph]:
    marker_factorization_graphs_by_size = {}
    if not fname_pdf_base.endswith(".pdf"):
        fname_pdf_base += ".pdf"

    for size, optimal_factors in optimal_factorizations_by_size.items():
        singleton_blocks = [x.flat_set for x in optimal_factors if x.is_singleton]
        long_blocks = [x.flat_set for x in optimal_factors if not x.is_singleton]
        igraph = primes2igraph(primes=markers.problem.primes)
        igraph.graph["edge"]["color"] = "gray"
        igraph.graph["label"] = "factorization = " + " * ".join(map(str, optimal_factors))
        igraph.graph["fontsize"] = 40

        if len(singleton_blocks) > 19:
            log.warning(f"number of blocks exceeds maximum number of colors, colors will repeat: n_blocks={len(singleton_blocks)}, n_colors=19")

        for x in range(igraph.order()):
            y = markers.problem.component_names[x]
            igraph.nodes[y]["fillcolor"] = None
            igraph.nodes[y]["label"] = f"{y}\n{x}"

        for i, block in enumerate(singleton_blocks):
            for x in block:
                y = markers.problem.component_names[x]
                igraph.nodes[y]["fillcolor"] = f"/pastel19/{i + 1}"
                igraph.nodes[y]["color"] = "black"

        for i, block in enumerate(long_blocks):
            for x in block:
                y = markers.problem.component_names[x]
                igraph.nodes[y]["fillcolor"] = "gray"
                igraph.nodes[y]["shape"] = "square"

        marker_factorization_graphs_by_size[size] = igraph
        fname_pdf = fname_pdf_base.replace(".pdf", f"_n{size}.pdf")
        igraph2image(igraph=igraph, fname_image=fname_pdf, layout_engine="dot")
        log.info(f"created {fname_pdf}")

    return marker_factorization_graphs_by_size

