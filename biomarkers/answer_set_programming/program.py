

import logging
import subprocess
from typing import List

from clingo import Model
from clingo.control import Control

log = logging.getLogger(__name__)


class Program:
    control: Control
    program: List[str]
    options: List[str]

    def __init__(self, options: List[str] = None):
        if options is None:
            options = ["--models=0", "--opt-mode=optN", "--enum-mode=domRec", "--heuristic=Domain", "--dom-mod=5,16"]

        self.program = []
        self.options = list(options)
        self.control = Control(arguments=self.options)

    def __repr__(self) -> str:
        return self.to_str()

    def add_lines(self, lines: List[str]):
        self.program.extend(lines)

    def add_line(self, line: str):
        self.add_lines([line])

    def show(self, predicate: str, arity: int):
        self.add_lines(lines=["% solver instructions", f"#show {predicate}/{arity}."])

    def solve(self) -> List[List[int]]:
        indices = []

        def on_model(model: Model):
            if model.optimality_proven:
                indices.append(sorted(symbol.number for symbol in model.symbols(shown=True)))
            else:
                indices.append(sorted(symbol.arguments[0].number for symbol in model.symbols(shown=True)))

        self.control.add(name="base", parameters={}, program="\n".join(self.program))
        self.control.ground(parts=[("base", [])])
        self.control.solve(on_model=on_model)

        print(f"$ clingo {' '.join(self.options)}")

        return indices

    def print_solve_result(self):
        print(f"control.is_conflicting={self.control.is_conflicting}")

    def solve_command_line(self, options: List[str] = None, time_limit_seconds=300):
        if options is None:
            options = ["clingo", "--models=0", f"--time-limit={time_limit_seconds}", "--opt-mode=optN", "--enum-mode=domRec", "--heuristic=Domain", "--dom-mod=5,16"]
        result = subprocess.run(options, input=self.to_str(), capture_output=True, text=True)
        print(result.stdout)
        print(f"$ clingo {' '.join(options)}")

    def to_asp(self, fname: str) -> str:
        text = self.to_str()

        with open(fname, "w") as fp:
            fp.write(text)

        log.info(f"created {fname}")

        return text

    def to_str(self) -> str:
        return "\n".join(self.program).replace("%", "\n%") + "\n"
