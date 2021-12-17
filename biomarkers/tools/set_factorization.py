from collections import defaultdict
from itertools import combinations
from math import prod
from typing import List, Set, Iterable, Dict

import pandas as pd

from biomarkers.answer_set_programming.program import Program
from biomarkers.marker_detection.markers import Markers

IntegerSets = List[Set[int]]


def factorize_marker_sets_and_print_result(markers: Markers):
    integer_sets_by_size = integer_sets_by_size_from_markers(markers=markers)
    factors_by_size = compute_factors_by_size(integer_sets_by_size=integer_sets_by_size)

    data = defaultdict(list)
    for size, factors in factors_by_size.items():
        data["n_marker_components"].append(size)
        data["n_markers"].append(len(integer_sets_by_size[size]))
        data["n_factors"].append(len(factors) if factors else None)
        data["product"].append(prod(map(len, factors)) if factors else None)

        if not factors:
            data["factors_dropped"].append("-")
            data["factorization"].append("-")
            continue

        factors_intersection_free = []
        for factor in factors:
            if not any(x.intersection(factor) for x in factors_intersection_free):
                factors_intersection_free.append(factor)

        if not validate_factorization(integer_sets=integer_sets_by_size[size], factors=factors_intersection_free):
            print(f"factorization is not valid: size={size}")

        data["factors_dropped"].append(",".join(factor_to_str(x) for x in factors if x not in factors_intersection_free))

        factors_union = set.union(*factors_intersection_free)
        cofactor = find_cofactor(integer_sets=integer_sets_by_size[size], factors_union=factors_union)
        product = prod(map(len, factors_intersection_free))
        sum_ = len(integer_sets_by_size[size])
        c = int(sum_ / product)

        if len(cofactor) != c:
            print(f"encountered error in factorization algorithm: size={size}, product={product}, sum={sum_}, cofactor={len(cofactor)}")

        data["factorization"].append(f"{' x '.join(factor_to_str(factor=factor) for factor in factors_intersection_free)}{f' x L({c})' if c != 1 else ''}")

    print(pd.DataFrame(data=data).convert_dtypes().to_string(index=False))


def factor_to_str(factor: Set[int]) -> str:
    return "{" + ",".join(f'{{{x}}}' for x in factor) + "}"


def compute_largest_factor(integer_sets: IntegerSets) -> Set[int]:
    program = Program(options=["--opt-mode=opt", "--models=0"])

    program.add_line(line="% integer sets")
    for i, set_ in enumerate(integer_sets):
        program.add_line(line=" ".join(f"s({i},{x})." for x in set_))

    program.add_line(line="% factor")
    program.add_line(line="{f(C) : s(_,C)}.")

    program.add_line(line="% factor must be unique in each integer set")
    program.add_line(line=":- s(I,C1), s(I,C2), f(C1), f(C2), C1!=C2.")

    program.add_line(line="% maximize factor")
    program.add_line(line="#maximize {C,f(C): s(I,C), f(C)}.")
    program.show(predicate="f", arity=1)

    print(program.to_str())

    largest_factor = program.solve()
    print(largest_factor)

    return {}


def find_cofactor(integer_sets: IntegerSets, factors_union: Set[int]) -> IntegerSets:
    return [set(x) for x in set([tuple(sorted(x.difference(factors_union))) for x in integer_sets])]


def find_remainder(integer_sets: IntegerSets, factor) -> IntegerSets:
    pass


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
        divisor_size = total / frequency
        if divisor_size == int(divisor_size):
            for combination in combinations(elements, r=int(divisor_size)):
                combination = set(combination)
                if is_set_factor(sets=integer_sets, candidate=combination):
                    factors.append(combination)

    return factors


def is_set_factor(sets: Iterable[Set[int]], candidate: Set[int]) -> bool:
    for s in sets:
        if len(s.intersection(candidate)) != 1:
            return False

    return True


def validate_factorization(integer_sets: IntegerSets, factors: IntegerSets) -> bool:
    from itertools import product

    assumed = set(tuple(sorted(x)) for x in product(*factors))
    given = set(tuple(sorted(x)) for x in integer_sets)

    return assumed == given


if __name__ == "__main__":
    from biomarkers.tools.marker_detection import try_to_load_markers_or_exit

    markers = try_to_load_markers_or_exit(fname="../../selvaggio/h3_markers.json")
    factorize_marker_sets_and_print_result(markers=markers)


if None is False:
    integer_sets = [{1, 3}, {2, 3}, {4, 6}, {5, 6}, {7, 8}]

    largest_factor = compute_largest_factor(integer_sets=integer_sets)
    largest_cofactor = find_cofactor(integer_sets=integer_sets, factors_union=largest_factor)
    remainder = find_remainder(integer_sets=integer_sets, factor=largest_factor)

    print(f"{largest_factor} x {largest_cofactor} + {remainder}")

