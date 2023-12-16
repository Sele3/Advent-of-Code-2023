from advent_of_code_solver import BaseSolver

from .utils import BeamGrid, D, L, R, U


class Solver(BaseSolver):
    def parse_input(self, file):
        return BeamGrid(file.read().splitlines())

    def solve_part1(self):
        grid: BeamGrid = self.input
        return grid.count_energized_tiles(0, 0, R)

    def solve_part2(self):
        grid: BeamGrid = self.input
        curr_max = 0

        for r in range(grid.m):
            curr_max = max(curr_max, grid.count_energized_tiles(r, 0, R))
            curr_max = max(curr_max, grid.count_energized_tiles(r, grid.n - 1, L))

        for c in range(grid.n):
            curr_max = max(curr_max, grid.count_energized_tiles(0, c, D))
            curr_max = max(curr_max, grid.count_energized_tiles(grid.m - 1, c, U))

        return curr_max
