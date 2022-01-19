

from itertools import product
from typing import Set, Iterable, Tuple


class IntegerSets:
    _sets: Tuple[Set[int]]

    def __init__(self, sets_of_integers: Iterable[Iterable[int]]):
        self._sets = tuple(set(x) for x in sorted(tuple(x for x in integers) for integers in sets_of_integers))

    def __iter__(self) -> Iterable[Set[int]]:
        return iter(set(x) for x in self._sets)

    def __len__(self) -> int:
        return len(self._sets)

    def __mul__(self, other: "IntegerSets") -> "IntegerSets":
        return IntegerSets(sets_of_integers=set(tuple(x.union(y)) for x, y in product(self, other)))

    def __eq__(self, other: "IntegerSets") -> bool:
        if len(self) != len(other):
            return False

        return all(x == y for x, y in zip(self, other))

    def __repr__(self) -> str:
        if not self._sets:
            return "EmptyIntegerSets"
        # return f"{{{','.join(str(x) for x in self._sets)}}}"

        if self.is_singleton:
            return f"S({','.join(str(x) for y in self for x in y)})"

        if len(self) < 4:
            return f"{{{','.join('{'+','.join(map(str,x))+'}' for x in self)}}}"

        return f"L(n={len(self._sets[0])},k={len(self._sets)})"

    @property
    def is_singleton(self) -> bool:
        return all(len(x) == 1 for x in self._sets)

    @property
    def flat_set(self) -> Set[int]:
        return set.union(*self._sets)

    def is_a_factor_of(self, other: "IntegerSets") -> bool:
        return all(sum(x.issubset(y) for x in self) == 1 for y in other)
