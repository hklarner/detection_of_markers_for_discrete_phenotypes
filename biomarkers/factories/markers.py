from biomarkers.factories.program import program_from_problem
from biomarkers.marker_detection.markers import Markers
from biomarkers.marker_detection.problem import Problem


def markers_from_problem(problem: Problem) -> Markers:
    """
    for future reference:

    ```
    if model.optimality_proven:
        indices.append(sorted(symbol.number for symbol in model.symbols(shown=True)))
    else:
        indices.append(sorted(symbol.arguments[0].number for symbol in model.symbols(shown=True)))
    ```
    """

    program = program_from_problem(problem=problem)
    indices = program.solve()
    markers = Markers(indices=indices, component_names=problem.component_names)

    return markers


if __name__ == "__main__":
    from biomarkers.tools.marker_detection import try_to_load_problem_or_exit

    markers = markers_from_problem(problem=try_to_load_problem_or_exit(fname="../../n7s3_problem.json"))
    pass
