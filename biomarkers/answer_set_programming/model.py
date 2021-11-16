

import logging
from typing import List

import subprocess
from clingo.control import Control
from clingo.solving import SolveResult
from clingo import Model as ClingoModel

from biomarkers.marker_detection.markers import Markers

log = logging.getLogger(__name__)


class Model:
    control: Control
    program: List[str]
    options: List[str]
    result: SolveResult = None

    def __init__(self, options: List[str] = None):
        if options is None:
            options = ["--models=0", "--opt-mode=optN", "--enum-mode=domRec", "--heuristic=Domain", "--dom-mod=5,16"]
        self.program = []
        self.options = list(options)
        self.control = Control(arguments=self.options)

    def __repr__(self) -> str:
        return "\n".join(self.program)

    def add_lines_to_program(self, lines: List[str]):
        self.program.extend(lines)

    def add_line_to_program(self, line: str):
        self.add_lines_to_program([line])

    def show(self, predicate: str, arity: int):
        self.add_lines_to_program(lines=["% solver instructions", f"#show {predicate}/{arity}."])

    def solve(self) -> Markers:
        indices = []

        def on_model(model: ClingoModel):
            if model.optimality_proven:
                indices.append(sorted(symbol.number for symbol in model.symbols(shown=True)))
            else:
                indices.append(sorted(symbol.arguments[0].number for symbol in model.symbols(shown=True)))

        self.control.add(name="base", parameters={}, program="\n".join(self.program))
        self.control.ground(parts=[("base", [])])
        self.result = self.control.solve(on_model=on_model)

        indices.sort()

        return Markers(indices=indices)

    def print_solve_result(self):
        print(f"control.is_conflicting={self.control.is_conflicting}")
        if self.result:
            print(f"result.satisfiable={self.result.satisfiable}")
            print(f"result.exhausted={self.result.exhausted}")

    def solve_command_line(self, options: List[str] = None):
        if options is None:
            options = ["clingo", "--models=0", "--time-limit=100", "--opt-mode=optN", "--enum-mode=domRec", "--heuristic=Domain", "--dom-mod=5,16"]
        result = subprocess.run(options, input="\n".join(self.program), capture_output=True, text=True)
        print(result.stdout)

    def to_asp(self, fname: str) -> str:
        with open(fname, "w") as fp:
            text = "\n".join(self.program).replace("%", "\n%")
            fp.write(text)

        log.info(f"created {fname}")

        return text
