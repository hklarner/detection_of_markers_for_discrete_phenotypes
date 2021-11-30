

import pytest

from biomarkers.factories.program import program_from_problem
from biomarkers.marker_detection.problem import Problem


@pytest.mark.parametrize("states,indices,family", [
    ([[0, 0], [0, 0]], [0, 1], []),
    ([[0, 0], [0, 0]], [1, 0], []),
    ([[0, 0], [0, 0]], [0, 0], [[0], [1]]),
    ([[0, 0], [0, 0]], [1, 1], [[0], [1]]),
    ([[0, 0], [0, 1]], [0, 1], [[1]]),
])
def test_two_steady_states_cases(states, indices, family):
    problem = Problem(steady_states=states, phenotype_indices=indices)
    model = program_from_problem(problem=problem)
    marker_family = model.solve()

    assert marker_family == family


