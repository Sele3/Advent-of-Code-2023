from multiprocessing import Pool, cpu_count

from advent_of_code_solver import BaseSolver

from .utils import BeamGrid, D, L, R, U


def process_row(starting_position, grid):
    """
    Helper function for multiprocessing
    """
    r, c, d = starting_position
    return grid.count_energized_tiles(r, c, d)


class Solver(BaseSolver):
    def parse_input(self, file):
        return BeamGrid(file.read().splitlines())

    def solve_part1(self):
        grid: BeamGrid = self.input
        return grid.count_energized_tiles(0, 0, R)

    def solve_part2(self):
        grid: BeamGrid = self.input

        starting_positions = (
            [(r, 0, R) for r in range(grid.m)]
            + [(r, grid.n - 1, L) for r in range(grid.m)]
            + [(0, c, D) for c in range(grid.n)]
            + [(grid.m - 1, c, U) for c in range(grid.n)]
        )

        with Pool(cpu_count()) as pool:
            results = pool.starmap(
                process_row, [(pos, grid) for pos in starting_positions]
            )

        return max(results)
