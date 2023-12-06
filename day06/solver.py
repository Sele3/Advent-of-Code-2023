import re
from collections import namedtuple
from functools import reduce
from operator import mul
from typing import List

from advent_of_code_solver import BaseSolver

Race = namedtuple("Race", ("time", "record"))


def count_ways_to_beat_record(race: Race) -> int:
    """
    Count the number of ways to beat the record.

    | Intuition
    | - We only need to check speeds from 1 to time // 2 + 1, since it is mirrored after that.
    | - Use binary search to find the minimum speed that can beat the record.
    | - The number of ways to beat the record is the number of speeds >= the minimum speed.
    | - If the time is even, we subtract 1 from the result as the speed and move time is the same value.
    """
    lo, hi = 1, race.time // 2 + 1

    while lo < hi:
        speed = (lo + hi) // 2
        move_time = race.time - speed

        if speed * move_time <= race.record:
            lo = speed + 1
        else:
            hi = speed

    # The number of ways to beat the record is the number of speeds >= the minimum speed, times 2.
    result = ((race.time // 2) - lo + 1) * 2
    # If the time is even, subtract 1 from the result as the speed and move time is the same value.
    return result if race.time % 2 else result - 1


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
