from collections import defaultdict
from typing import Dict, List

from advent_of_code_solver import BaseSolver


class Solver(BaseSolver):
    def parse_input(self, file):
        # Build a graph from the input
        result = defaultdict(list)
        for line in file.read().splitlines():
            curr, others = line.split(": ")
            for other in others.split(" "):
                result[curr].append(other)
                result[other].append(curr)

        return result

    def solve_part1(self):
        g: Dict[str, List[str]] = self.input
        not_connected = {k: 0 for k in g.keys()}
        connected = set()
        total = 0

        while total != 3:
            most_common = max(not_connected, key=not_connected.get)
            connected.add(most_common)
            total -= not_connected.pop(most_common)

            for v in g[most_common]:
                if v in not_connected:
                    not_connected[v] += 1
                    total += 1

        return len(not_connected) * len(connected)

    def solve_part2(self):
        return "Merry Christmas!"
