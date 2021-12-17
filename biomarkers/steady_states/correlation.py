

from collections import defaultdict
from itertools import combinations
from typing import List


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
