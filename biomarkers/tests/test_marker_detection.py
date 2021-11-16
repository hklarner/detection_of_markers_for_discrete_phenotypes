

import pytest

from biomarkers.marker_detection.problem import Problem
from biomarkers.factories.model import model_from_problem


@pytest.mark.parametrize("states,indices,family", [
    ([[0, 0], [0, 0]], [0, 1], []),
    ([[0, 0], [0, 0]], [1, 0], []),
    ([[0, 0], [0, 0]], [0, 0], [[0], [1]]),
    ([[0, 0], [0, 0]], [1, 1], [[0], [1]]),
    ([[0, 0], [0, 1]], [0, 1], [[1]]),
])
def test_two_steady_states_cases(states, indices, family):
    problem = Problem(steady_states=states, phenotype_indices=indices)
    model = model_from_problem(problem=problem)
    marker_family = model.solve()

    assert marker_family == family


