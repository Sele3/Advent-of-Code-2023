import re
from collections import namedtuple
from functools import reduce
from math import ceil, floor, sqrt
from operator import mul
from typing import List

from advent_of_code_solver import BaseSolver

Race = namedtuple("Race", ("time", "record"))


def count_ways_to_beat_record(race: Race) -> int:
    """
    Count the number of ways to beat the record. Use quadratic formula to find
    the range of speeds that can beat the record.

    | Formula:
    | - x = speed to find, t = race time, r = race record
    | - we want to find x such that x * (t - x) > r
    | - rearrange to get x^2 - tx + r < 0, therefore a = 1, b = -t, c = r
    """

    b, c = -race.time, race.record
    # discriminant
    d = b**2 - 4 * c

    # solve for roots
    low_root = (-b - sqrt(d)) / 2.0
    high_root = (-b + sqrt(d)) / 2.0

    # find the range of speeds that can beat the record
    # if the root is an integer, we add/subtract 1 to find strictly greater/less than
    min_speed = int(low_root) + 1 if int(low_root) == low_root else ceil(low_root)
    max_speed = int(high_root) - 1 if int(high_root) == high_root else floor(high_root)
    return max_speed - min_speed + 1


class Solver(BaseSolver):
    def parse_input(self, file):
        times, records = file.read().splitlines()
        times = [int(x) for x in re.findall(r"\d+", times)]
        records = [int(x) for x in re.findall(r"\d+", records)]

        return [Race(time, record) for time, record in zip(times, records)]

    def solve_part1(self):
        races: List[Race] = self.input
        return reduce(mul, (count_ways_to_beat_record(race) for race in races))

    def solve_part2(self):
        races: List[Race] = self.input
        concat_time = "".join(str(race.time) for race in races)
        concat_record = "".join(str(race.record) for race in races)

        new_race = Race(int(concat_time), int(concat_record))
        return count_ways_to_beat_record(new_race)
