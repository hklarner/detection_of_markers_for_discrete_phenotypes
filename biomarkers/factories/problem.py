

from typing import Optional

from biomarkers.marker_detection.problem import Problem

from pyboolnet.trap_spaces import steady_states as compute_steady_states


def problem_from_primes(primes: dict, max_steady_states: int = 10000, max_marker_size: Optional[int] = None) -> Problem:
    steady_states = [list(map(int, x)) for x in compute_steady_states(primes=primes, max_output=max_steady_states, representation="str")]
    problem = Problem(steady_states=steady_states, max_marker_size=max_marker_size)

    return problem


if __name__ == "__main__":
    x = "010101101111"
    print(list(map(int, x)))
