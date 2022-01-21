

import sys
from collections import defaultdict
from typing import Optional

import pandas as pd
from networkx import DiGraph
from pyboolnet.interaction_graphs import igraph2image
from pyboolnet.interaction_graphs import primes2igraph

from biomarkers.marker_detection.markers import Markers


def create_marker_count_graph(markers: Markers, component_counts: pd.DataFrame, fname_pdf: Optional[str] = None) -> DiGraph:
    igraph = primes2igraph(primes=markers.problem.primes)
    igraph.graph["edge"]["color"] = "gray"
    igraph.graph["label"] = f"n_marker_sets={len(markers.indices)}\nk: count\np: likelihood"
    igraph.graph["fontsize"] = 40

    for i, row in component_counts.iterrows():
        igraph.nodes[row["name"]]["fillcolor"] = f"0.1 {row['likelihood']+0.2:.1f} 1.0"
        igraph.nodes[row["name"]]["label"] = f"{row['name']}\nk={row['count']}\np={row['likelihood']:.1f}"

    if markers.problem.phenotype_components:
        for node in markers.problem.phenotype_components:
            node_name = markers.problem.component_names[node]
            igraph.nodes[node_name]["fillcolor"] = "0.6 0.5 1.0"

    if fname_pdf:
        igraph2image(igraph=igraph, fname_image=fname_pdf, layout_engine="dot")
        print(f"created {fname_pdf}")

    return igraph


def get_component_counts_from_markers(markers: Markers) -> pd.DataFrame:
    counts = defaultdict(int)
    for indices in markers.indices:
        for x in indices:
            counts[x] += 1

    total = len(markers.indices)
    data = defaultdict(list)
    for x, count in sorted(counts.items()):
        node_name = markers.problem.component_names[x]
        data["index"].append(x)
        data["name"].append(node_name)
        data["count"].append(count)
        data["likelihood"].append(count / total)

    df = pd.DataFrame(data=data)

    return df


if __name__ == "__main__":
    from pyboolnet.repository import get_primes

    from biomarkers.tools.marker_detection import try_to_load_markers_or_exit
    from biomarkers.tools.validation import assert_consistency_of_component_names_or_exit

    primes = get_primes(name="selvaggio_emt")
    markers = try_to_load_markers_or_exit(fname="../../markers.json")
    assert_consistency_of_component_names_or_exit(primes=primes, markers=markers)

    sys.exit()
