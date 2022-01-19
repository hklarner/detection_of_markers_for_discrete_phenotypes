

from typing import List, Dict


def phenotype_indices_from_subspace(steady_states: List[List[int]], phenotype_subspace: Dict[int, int]) -> List[int]:
    phenotype_indices = [1 if all(x[k] == phenotype_subspace[k] for k in phenotype_subspace) else 0 for x in steady_states]

    return phenotype_indices


def phenotype_indices_from_components(steady_states: List[List[int]], phenotype_components: List[int]) -> List[int]:
    phenotypes = []
    phenotype_indices = []

    for state in steady_states:
        phenotype = tuple(state[x] for x in phenotype_components)
        if phenotype not in phenotypes:
            phenotypes.append(phenotype)
        phenotype_indices.append(phenotypes.index(phenotype))

    phenotype_indices = phenotype_indices

    return list(phenotype_indices)


if __name__ == "__main__":
    x = "010101101111"
    print(list(map(int, x)))
