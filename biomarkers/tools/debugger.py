

from typing import Optional

from biomarkers.answer_set_programming.model import Model


def debug_by_relaxation(model: Model, assumption: Optional[str]):
    for line in model.program:
        if "%" in line or "show" in line:
            continue

        if line.count(".") > 10:
            continue

        new_program = list(model.program)
        new_program.remove(line)
        options = ["--models=0", "--opt-mode=optN", "--enum-mode=domRec", "--heuristic=Domain", "--dom-mod=5,16"]
        options = []
        new_model = Model(options=options)

        if assumption:
            new_model.add_lines_to_program(lines=["% debugging assumption", assumption])

        markers = new_model.solve()

        if markers != [[]]:
            print(f"found relaxation that is satisfiable")
            print(line)
            print(markers[0])
            print(f"{len(markers)=}")
            print(model.print_solve_result())
