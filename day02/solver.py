from collections import Counter
from functools import reduce
from typing import List

from advent_of_code_solver import BaseSolver

RED = "red"
GREEN = "green"
BLUE = "blue"


def get_cubes_power(subsets: List[Counter]) -> int:
    """
    Get the fewest number of cubes required to make the game, then find the power of the set of cubes.
    :return: The set power, which is the product of the number of cubes of each color.
    """
    required = reduce(lambda x, y: x | y, subsets)
    return required[RED] * required[GREEN] * required[BLUE]


class Solver(BaseSolver):
    def parse_input(self, file):
        return [
            self._get_subset_list(line.split(": ")[1])
            for line in file.read().splitlines()
        ]

    def solve_part1(self):
        bag = Counter({RED: 12, GREEN: 13, BLUE: 14})
        return sum(
            game_id
            for game_id, game in enumerate(self.input, start=1)
            if all(bag >= subset for subset in game)
        )

    def solve_part2(self):
        return sum(get_cubes_power(game) for game in self.input)

    @staticmethod
    def _get_subset_list(line: str) -> List[Counter]:
        result = []

        for subset in line.split("; "):
            cubes = Counter({RED: 0, GREEN: 0, BLUE: 0})

            for color in subset.split(", "):
                num, color = color.split(" ")
                cubes[color] += int(num)

            result.append(cubes)

        return result
