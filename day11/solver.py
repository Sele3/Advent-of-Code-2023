from typing import List

from advent_of_code_solver import BaseSolver

from .utils import GalaxyImage


class Solver(BaseSolver):
    def parse_input(self, file):
        grid: List[str] = file.read().splitlines()
        return GalaxyImage(grid)

    def solve_part1(self):
        image: GalaxyImage = self.input
        return image.calculate_total_path_distance()

    def solve_part2(self):
        image: GalaxyImage = self.input
        image.times_larger = 1_000_000
        return image.calculate_total_path_distance()
