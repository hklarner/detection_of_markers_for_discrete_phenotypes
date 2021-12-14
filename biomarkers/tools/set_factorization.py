

from collections import defaultdict
from itertools import combinations
from math import prod
from typing import List, Set, Iterable, Dict

import pandas as pd

from biomarkers.marker_detection.markers import Markers


def factorize_marker_sets_and_print_result(markers: Markers):
    marker_sets_by_size = create_marker_sets_by_size(markers=markers)
    factorizations_by_size = factorize_marker_sets_by_size(marker_sets_by_size=marker_sets_by_size)

    data = defaultdict(list)
    for size, factors in factorizations_by_size.items():
        data["n_marker_components"].append(size)
        data["n_markers"].append(len(marker_sets_by_size[size]))
        data["n_factors"].append(len(factors) if factors else None)
        data["product"].append(prod(map(len, factors)) if factors else None)

    print(pd.DataFrame(data=data).convert_dtypes().to_string(index=False))

    for size, factors in factorizations_by_size.items():
        if not factors:
            print(f"{size:< 2}: -")
            continue

        product = prod(map(len, factors))
        sum_ = len(marker_sets_by_size[size])
        remainder = sum_ - product

        print(f"{size:< 2}: {' x '.join(f'{{{s}}}' for s in factors)}{f' + Remainder({remainder})' if remainder else ''}")


def create_marker_sets_by_size(markers: Markers) -> Dict[int, List[Set[int]]]:
    marker_sets_by_size = defaultdict(list)
    for marker_list in markers.indices:
        marker_sets_by_size[len(marker_list)].append(set(marker_list))

    return marker_sets_by_size


def factorize_marker_sets_by_size(marker_sets_by_size: Dict[int, List[Set[int]]]) -> Dict[int, List[Set[int]]]:
    set_factorizations = defaultdict(list)
    for size, marker_sets in marker_sets_by_size.items():
        set_factorizations[size] = factorize_marker_sets(marker_sets=marker_sets)

    return set_factorizations


def factorize_marker_sets(marker_sets: List[Set[int]]) -> List[Set[int]]:
    element_counts = defaultdict(int)
    for marker_set in marker_sets:
        for e in marker_set:
            element_counts[e] += 1

    frequencies = defaultdict(list)
    for element, count in element_counts.items():
        frequencies[count].append(element)

    total = len(marker_sets)

    set_factors = []
    for frequency, elements in frequencies.items():
        divisor_size = total / frequency
        if divisor_size == int(divisor_size):
            for combination in combinations(elements, r=int(divisor_size)):
                combination = set(combination)
                if is_set_factor(sets=marker_sets, candidate=combination):
                    set_factors.append(combination)

    return set_factors


def is_set_factor(sets: Iterable[Set[int]], candidate: Set[int]) -> bool:
    for s in sets:
        if len(s.intersection(candidate)) != 1:
            return False

    return True
