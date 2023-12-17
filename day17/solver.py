from advent_of_code_solver import BaseSolver

from .utils import CityMap


class Solver(BaseSolver):
    def parse_input(self, file):
        grid = [list(map(int, line)) for line in file.read().splitlines()]
        return CityMap(grid)

    def solve_part1(self):
        city_map: CityMap = self.input
        return city_map.get_least_incurred_loss(1, 3)

    def solve_part2(self):
        city_map: CityMap = self.input
        return city_map.get_least_incurred_loss(4, 10)
