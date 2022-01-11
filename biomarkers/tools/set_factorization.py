

from collections import defaultdict
from itertools import combinations, product
from math import prod
from typing import List, Set, Iterable, Dict

import pandas as pd

from biomarkers.marker_detection.markers import Markers

IntegerSets = List[Set[int]]


def factorize_marker_sets(markers: Markers) -> pd.DataFrame:
    integer_sets_by_size = integer_sets_by_size_from_markers(markers=markers)
    factors_by_size = compute_factors_by_size(integer_sets_by_size=integer_sets_by_size)

    data = defaultdict(list)
    for size, factors in factors_by_size.items():
        integer_sets = integer_sets_by_size[size]
        data["n_components"].append(size)
        data["n_markers"].append(len(integer_sets))

        if factors:
            checksum = prod(map(len, factors))
            missing_factor = find_missing_factor(integer_sets=integer_sets, factors=factors)
            if missing_factor:
                checksum *= len(missing_factor)

            if len(integer_sets) == checksum:
                data["factors"].append(", ".join(str(list(x)) for x in factors))
                data["len(missing_factor)"].append(len(missing_factor))
                continue

        data["factors"].append("-")
        data["len(missing_factor)"].append("-")

    df = pd.DataFrame(data=data).convert_dtypes()

    return df


def validate_factorization(integer_sets: IntegerSets, factors: IntegerSets, missing_factor: IntegerSets) -> bool:
    left_hand_side = set(tuple(sorted(x)) for x in integer_sets)
    right_hand_side = set(tuple(sorted(x)) for x in product(*factors))


def find_missing_factor(integer_sets: IntegerSets, factors: IntegerSets) -> IntegerSets:
    factors_union = set.union(*factors)
    last_factor = set()

    for integer_set in integer_sets:
        diff = integer_set.difference(factors_union)
        if diff:
            last_factor.add(tuple(sorted(diff)))

    last_factor = [set(x) for x in last_factor]

    return last_factor


def integer_sets_by_size_from_markers(markers: Markers) -> Dict[int, IntegerSets]:
    integer_sets_by_size = defaultdict(list)
    for marker_list in markers.indices:
        integer_sets_by_size[len(marker_list)].append(set(marker_list))

    return integer_sets_by_size


def compute_factors_by_size(integer_sets_by_size: Dict[int, IntegerSets]) -> Dict[int, IntegerSets]:
    factors_by_size = defaultdict(list)
    for size, integer_sets in integer_sets_by_size.items():
        factors_by_size[size] = compute_factors(integer_sets=integer_sets)

    return factors_by_size


def compute_factors(integer_sets: IntegerSets) -> IntegerSets:
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
        if remainder == 0:
            for combination in combinations(elements, r=quotient):
                combination = set(combination)
                if factor_intersects_each_set_once(sets=integer_sets, factor=combination):
                    factors.append(combination)

    return factors


def factor_intersects_each_set_once(sets: Iterable[Set[int]], factor: Set[int]) -> bool:
    return all(len(factor.intersection(s)) == 1 for s in sets)


def integer_sets_are_equal_to_product_of_factors(integer_sets: IntegerSets, factors: IntegerSets) -> bool:
    assumed = set(tuple(sorted(x)) for x in product(*factors))
    given = set(tuple(sorted(x)) for x in integer_sets)

    return assumed == given


if __name__ == "__main__":
    from biomarkers.tools.marker_detection import try_to_load_markers_or_exit

    markers = try_to_load_markers_or_exit(fname="../../selvaggio/run_selvaggio/m1_markers.json")
    df = factorize_marker_sets(markers=markers)

    #print(df.to_latex())
    print(df.to_string())

