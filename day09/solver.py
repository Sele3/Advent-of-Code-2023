from itertools import pairwise
from typing import List

from advent_of_code_solver import BaseSolver


def extrapolate(nums: List[int]) -> int:
    """
    Extrapolate a list of numbers by adding the difference between each number
    """
    if all(num == 0 for num in nums):
        return 0

    diffs = [b - a for a, b in pairwise(nums)]
    return nums[-1] + extrapolate(diffs)


class Solver(BaseSolver):
    def parse_input(self, file):
        return [list(map(int, line.split())) for line in file.readlines()]

    def solve_part1(self):
        return sum(extrapolate(nums) for nums in self.input)

    def solve_part2(self):
        return sum(extrapolate(nums[::-1]) for nums in self.input)
