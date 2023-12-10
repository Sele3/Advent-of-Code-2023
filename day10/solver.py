from advent_of_code_solver import BaseSolver

from .utils import PipeField


class Solver(BaseSolver):
    def parse_input(self, file):
        result = []
        start_r = start_c = -1
        # Convert the input to a format that's easier to work with
        translation = str.maketrans("|-LJ7F", "│─└┘┐┌")

        for r, line in enumerate(file.readlines()):
            if "S" in line:
                start_r, start_c = r, line.index("S")
            result.append(line.strip().translate(translation))

        return PipeField(result, start_r, start_c)

    def solve_part1(self):
        field: PipeField = self.input
        # The number of steps to reach the furthest point is half the number of loops
        return len(field.main_loops) // 2

    def solve_part2(self):
        field: PipeField = self.input
        return field.get_enclosed_area()
