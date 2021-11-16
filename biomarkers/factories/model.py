

from typing import List, Optional

from biomarkers.marker_detection.problem import Problem
from biomarkers.answer_set_programming.model import Model


def model_from_problem(problem: Problem) -> Model:
    model = Model()

    add_steady_state_data(model=model, problem=problem)
    add_marker_definition(model=model, problem=problem)
    add_phenotype_definition(model=model, problem=problem)
    add_consistency(model=model, problem=problem)
    model.show(predicate="m", arity=1)

    return model


def add_consistency(problem: Problem, model: Model):
    if problem.enable_one_to_one_consistency:
        lines = ["% defines 1-to-1 consistency between markers and phenotypes",
                 ":- different_marker_type(S1,S2), not different_phenotype(S1,S2)."]
    else:
        lines = ["% defines 1-to-many consistency between markers and phenotypes"]

    lines.append(":- different_phenotype(S1,S2), not different_marker_type(S1,S2).")

    model.add_lines_to_program(lines=lines)


def add_steady_state_data(model: Model, problem: Problem):
    model.add_line_to_program("% defines the steady states")
    model.add_line_to_program("\n".join([" ".join(f"x({i},{c},{a})." for c, a in enumerate(state)) for i, state in enumerate(problem.steady_states)]))


def add_marker_definition(model: Model, problem: Problem):
    pre = f"{problem.min_marker_size} " if problem.min_marker_size is not None else ""
    post = f" {problem.max_marker_size}" if problem.max_marker_size is not None else ""

    lines = ["% defines the marker space"]
    if problem.forbidden_marker_components:
        lines.extend([
            " ".join(f"forbidden_marker_component({c})." for c in sorted(problem.forbidden_marker_components)),
            f"{pre}{{m(C): x(_,C,_), not forbidden_marker_component(C)}}{post}."])

    else:
        lines.append(f"{pre}{{m(C): x(_,C,_)}}{post}.")

    lines.extend([
        "% defines the marker type relation",
        "different_marker_type(S1,S2) :- x(S1,C,1), x(S2,C,0), m(C).",
        "different_marker_type(S1,S2) :- x(S1,C,0), x(S2,C,1), m(C).",
        "different_marker_type(S1,S2) :- different_marker_type(S2,S1)."
    ])

    model.add_lines_to_program(lines=lines)


def add_phenotype_definition(model: Model, problem: Problem):
    lines = []
    if problem.phenotype_components:
        lines.extend([
            "% defines the phenotype components"
            " ".join(f"phenotype_component({p})." for p in problem.phenotype_components),
            "% defines the phenotype relation",
            "different_phenotype(S1,S2) :- x(S1,C,1), x(S2,C,0), phenotype_component(C).",
            "different_phenotype(S1,S2) :- x(S1,C,0), x(S2,C,1), phenotype_component(C)."
        ])
    else:
        lines.extend([
            "% defines the indexed phenotypes",
            " ".join(f"p({i},{p})." for i, p in enumerate(problem.phenotype_indices)),
            "% defines the phenotype relation",
            "different_phenotype(S1,S2) :- p(S1,P1), p(S2,P2), P1!=P2."])

    lines.append("different_phenotype(S1,S2) :- different_phenotype(S2,S1).")
    model.add_lines_to_program(lines=lines)


