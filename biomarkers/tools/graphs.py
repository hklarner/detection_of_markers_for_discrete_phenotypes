

import sys
from collections import defaultdict
from typing import Dict, Optional

import pandas as pd
from networkx import DiGraph
from pyboolnet.interaction_graphs import igraph2image
from pyboolnet.interaction_graphs import primes2igraph

from biomarkers.marker_detection.markers import Markers
from biomarkers.pyboolnet_extensions import add_style_cascades


def create_marker_frequency_graph(markers: Markers, fname: Optional[str] = None) -> DiGraph:
    frequencies = component_frequencies_from_markers(markers=markers)
    total = len(markers.indices)
    fillcolor = "0.1 {:.1f} 1.0"

    igraph = primes2igraph(primes=markers.problem.primes)
    igraph.graph["edge"]["color"] = "gray"
    igraph.graph["label"] = f"Marker frequencies and cascades\nlen(markers)={total}"
    igraph.graph["fontsize"] = 40
    add_style_cascades(igraph=igraph)

    data = defaultdict(list)

    for node, frequency in frequencies.items():
        perc = frequency / total
        node_name = markers.problem.component_names[node]
        igraph.nodes[node_name]["fillcolor"] = fillcolor.format(perc)
        igraph.nodes[node_name]["label"] = f"{node_name}\nk={frequency}\np={perc:.1f}"

        data["name"].append(node_name)
        data["count"].append(frequency)
        data["likelihood"].append(perc)

    if fname:
        igraph2image(igraph=igraph, fname_image=fname, layout_engine="dot")

    print(pd.DataFrame(data=data))

    return igraph


def component_frequencies_from_markers(markers: Markers) -> Dict[int, int]:
    frequencies = defaultdict(int)
    for indices in markers.indices:
        for x in indices:
            frequencies[x] += 1

    return dict(frequencies)


if __name__ == "__main__":
    from pyboolnet.repository import get_primes

    from biomarkers.tools.marker_detection import try_to_load_markers_or_exit
    from biomarkers.tools.validation import assert_consistency_of_component_names_or_exit

    #  selvaggio_m1_

    primes = get_primes(name="selvaggio_emt")
    markers = try_to_load_markers_or_exit(fname="../../markers.json")
    assert_consistency_of_component_names_or_exit(primes=primes, markers=markers)
    create_marker_frequency_graph(primes=primes, markers=markers, fname="../../marker_frequency_graph.pdf")

    sys.exit()


