

from biomarkers.tools.marker_detection import try_to_load_problem_or_exit


if __name__ == "__main__":
    problem = try_to_load_problem_or_exit(fname="../marker_problem.json")
    print(list(problem.component_names[x] for x in [39, 15, 55]))
