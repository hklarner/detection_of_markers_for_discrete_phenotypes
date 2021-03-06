

import logging
from collections import defaultdict
from itertools import combinations, product
from typing import List, Dict

import networkx as nx
import pandas as pd

from biomarkers.marker_detection.markers import Markers
from biomarkers.tools.files import export_df
from biomarkers.tools.integer_sets import IntegerSets

log = logging.getLogger(__name__)


def factorize_marker_sets(markers: Markers, fname_tex: str, print_results: bool = True) -> Dict[int, List[IntegerSets]]:
    integer_sets_by_size = integer_sets_by_size_from_markers(markers=markers)
    factors_by_size = compute_factors_by_size(integer_sets_by_size=integer_sets_by_size)
    optimal_factors_by_size = {}

    data = defaultdict(list)
    for size, factors in factors_by_size.items():
        integer_sets = integer_sets_by_size[size]
        n_integer_sets = len(integer_sets)
        data["n_components"].append(size)
        data["n_markers"].append(n_integer_sets)

        if factors:
            for factor in factors:
                log.debug(f"{size} {factor}")

            missing_factor = find_missing_factor(integer_sets=integer_sets, factors=factors)
            log.debug(f"missing_factor = {missing_factor}")

            available_factors = list(factors) + ([missing_factor] if missing_factor else [])
            optimal_factors = compute_optimal_factors_for_factorization(sets=integer_sets, factors=available_factors)

            if optimal_factors:
                data["factorization"].append(" * ".join(map(str, optimal_factors)))
                data["n_factors_used"].append(len(optimal_factors))
                data["n_factors_available"].append(len(available_factors))
                optimal_factors_by_size[size] = optimal_factors
                continue

        data["factorization"].append("-")
        data["n_factors_used"].append("-")
        data["n_factors_available"].append("-")

    df = pd.DataFrame(data=data).convert_dtypes()

    if print_results:
        print(df.to_string(index=False))

    if fname_tex:
        export_df(df=df, fname=fname_tex, drop_columns=["n_factors_used", "n_factors_available"])

    return optimal_factors_by_size


def compute_optimal_factors_for_factorization(sets: IntegerSets, factors: List[IntegerSets]) -> List[IntegerSets]:
    independent_factors_graph = nx.Graph()
    for i, factor in enumerate(factors):
        independent_factors_graph.add_node(i, weight=len(factor))

    for i, j in combinations(range(len(factors)), r=2):
        if (factors[i] * factors[j]).is_a_factor_of(sets):
            independent_factors_graph.add_edge(i, j)

    clique, weight = nx.clique.max_weight_clique(independent_factors_graph)
    optimal_factors = sorted((factors[x] for x in clique if factors[x].is_singleton), key=lambda x: len(x)) + [factors[x] for x in clique if not factors[x].is_singleton]

    return optimal_factors


def find_missing_factor(integer_sets: IntegerSets, factors: List[IntegerSets]) -> IntegerSets:
    factors_union = set.union(*[y for x in factors for y in x])
    last_factor = set()

    for integer_set in integer_sets:
        diff = integer_set.difference(factors_union)
        if diff:
            last_factor.add(tuple(sorted(diff)))

    last_factor = IntegerSets(sets_of_integers=[x for x in last_factor])

    return last_factor


def integer_sets_by_size_from_markers(markers: Markers) -> Dict[int, IntegerSets]:
    marker_lists_by_size = defaultdict(list)
    for marker_list in markers.indices:
        marker_lists_by_size[len(marker_list)].append(marker_list)

    integer_sets_by_size = {size: IntegerSets(sets_of_integers=marker_lists) for size, marker_lists in marker_lists_by_size.items()}

    return integer_sets_by_size


def compute_factors_by_size(integer_sets_by_size: Dict[int, IntegerSets]) -> Dict[int, List[IntegerSets]]:
    factors_by_size = defaultdict(list)
    for size, integer_sets in integer_sets_by_size.items():
        factors_by_size[size] = compute_factors(integer_sets=integer_sets)

    return factors_by_size


def compute_factors(integer_sets: IntegerSets) -> List[IntegerSets]:
    element_counts = defaultdict(int)
    for integer_set in integer_sets:
        for e in integer_set:
            element_counts[e] += 1

    frequencies = defaultdict(list)
    for element, count in element_counts.items():
        frequencies[count].append(element)

    total = len(integer_sets)

    factors = []
    for frequency, elements in frequencies.items():
        quotient, remainder = divmod(total, frequency)
        if remainder == 0 and quotient <= len(elements):
            for integers in combinations(elements, r=quotient):
                factor = IntegerSets(sets_of_integers=[[x] for x in integers])
                if factor.is_a_factor_of(integer_sets):
                    factors.append(factor)

    return factors


def integer_sets_are_equal_to_product_of_factors(integer_sets: IntegerSets, factors: IntegerSets) -> bool:
    assumed = set(tuple(sorted(x)) for x in product(*factors))
    given = set(tuple(sorted(x)) for x in integer_sets)

    return assumed == given


if __name__ == "__main__":
    import sys
    from biomarkers.tools.marker_detection import try_to_load_markers_or_exit

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG, force=True)

    markers = try_to_load_markers_or_exit(fname="../../selvaggio/autogenerated/h1_markers.json")
    df = factorize_marker_sets(markers=markers)

    #print(df.to_latex())
    print(df.to_string())

