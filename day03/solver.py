from advent_of_code_solver import BaseSolver

from .utils import Schematic


class Solver(BaseSolver):
    def parse_input(self, file):
        grid = [line.strip() for line in file.read().splitlines()]
        return Schematic(grid)

    def solve_part1(self):
        schematic: Schematic = self.input
        return sum(schematic.part_numbers)

    def solve_part2(self):
        schematic: Schematic = self.input
        return sum(schematic.gear_ratios)
