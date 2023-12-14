import importlib
from datetime import datetime
from timeit import default_timer as timer

DAY_COUNT = datetime.today().day


def create_solver(day_str: str, input_file):
    module_name = f"day{day_str}.solver"
    module = importlib.import_module(module_name)

    solver_class = getattr(module, "Solver")
    return solver_class(input_file)


if __name__ == "__main__":
    day_str = str(DAY_COUNT).zfill(2)
    input_file = f"day{day_str}/input.txt"

    start = timer()

    try:
        solver = create_solver(day_str, input_file)
        solver.read_input_file()
    except Exception as e:
        print(e)
        exit(1)

    part1_solution = solver.solve_part1()
    print(f"Part 1 Solution: {part1_solution}")

    part2_solution = solver.solve_part2()
    print(f"Part 2 Solution: {part2_solution}")

    end = timer()
    print(f"Time Elapsed: {end - start}")
