import re
from typing import List

from advent_of_code_solver import BaseSolver

from .utils import CategoryMapper, CategoryRange


class Solver(BaseSolver):
    def parse_input(self, file):
        data = file.read().split("\n\n")

        seeds = re.findall(r"\d+", data[0])
        seeds = list(map(int, seeds))

        dummy_mapper = CategoryMapper([])
        for line in data[1:]:
            line = line.splitlines()
            ranges = []

            for nums in line[1:]:
                [dest_start, src_start, range_len] = map(int, nums.split())
                ranges.append(CategoryRange(dest_start, src_start, range_len))

            mapper = CategoryMapper(ranges)
            dummy_mapper.set_next_mapper(mapper)

        return seeds, dummy_mapper.next_mapper

    def solve_part1(self):
        seeds, base_mapper = self.input
        return min(map(base_mapper.map, seeds))

    def solve_part2(self):
        seeds, base_mapper = self.input
        ranges: List[range] = []

        # convert seeds to seed ranges
        for idx in range(0, len(seeds), 2):
            ranges.append(range(seeds[idx], seeds[idx] + seeds[idx + 1]))

        mapped_ranges = base_mapper.map_ranges(ranges)
        return min(map(lambda r: r.start, mapped_ranges))
