import importlib


def create_solver(day_number, input_file):
    module_name = f"day{day_number}.solver"

    try:
        module = importlib.import_module(module_name)
        solver_class = getattr(module, "Solver")
        return solver_class(input_file)
    except (ModuleNotFoundError, AttributeError):
        raise ValueError(f"No solver implemented for day {day_number}")


if __name__ == "__main__":
    day_number = 1
    input_file = f"day{day_number}/input.txt"

    try:
        solver = create_solver(day_number, input_file)
        solver.read_input_file()
    except Exception as e:
        print(e)
        exit(1)

    part1_solution = solver.solve_part1()
    print(f"Part 1 Solution: {part1_solution}")

    part2_solution = solver.solve_part2()
    print(f"Part 2 Solution: {part2_solution}")
