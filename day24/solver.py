import re
from collections import namedtuple
from itertools import combinations
from typing import List, Optional, Tuple

import z3

from advent_of_code_solver import BaseSolver

# Represents a Hailstone in 3D space
Hailstone = namedtuple("Hailstone", ("px", "py", "pz", "vx", "vy", "vz"))
# Represents a 2D line with gradient m and y-intercept c
Line2D = namedtuple("Line2D", ("m", "c"))


def to_line2D(h: Hailstone) -> Line2D:
    """
    Convert a Hailstone to a 2D line
    """
    m = h.vy / h.vx
    c = h.py - m * h.px
    return Line2D(m, c)


def get_xy_intersection(h1: Hailstone, h2: Hailstone) -> Optional[Tuple[int, int]]:
    """
    Get the intersection of two Hailstones in 2D space
    :return: A tuple of (x, y) coordinates of the intersection, or None if the lines are parallel
    """
    line1, line2 = to_line2D(h1), to_line2D(h2)
    # Parallel lines
    if line1.m == line2.m:
        return None

    x = (line2.c - line1.c) / (line1.m - line2.m)
    y = line1.m * x + line1.c
    return x, y


class Solver(BaseSolver):
    def parse_input(self, file):
        return [
            Hailstone(*map(int, re.findall(r"-?\d+", line)))
            for line in file.readlines()
        ]

    def solve_part1(self):
        test_min, test_max = 200000000000000, 400000000000000
        result = 0

        for h1, h2 in combinations(self.input, 2):
            # Parallel lines
            if (intersection := get_xy_intersection(h1, h2)) is None:
                continue

            cx, cy = intersection
            # Intersection occurred in the past
            if not ((cx > h1.px) == (h1.vx > 0) and (cx > h2.px) == (h2.vx > 0)):
                continue

            # Check if intersection is within test bounds
            if test_min <= cx <= test_max and test_min <= cy <= test_max:
                result += 1

        return result

    def solve_part2(self):
        hailstones: List[Hailstone] = self.input
        pxr, pyr, pzr, vxr, vyr, vzr = z3.Reals("pxr pyr pzr vxr vyr vzr")
        solver = z3.Solver()

        for k, h in enumerate(hailstones[:3]):
            t = z3.Real(f"t{k}")
            solver.add(pxr + t * vxr == h.px + t * h.vx)
            solver.add(pyr + t * vyr == h.py + t * h.vy)
            solver.add(pzr + t * vzr == h.pz + t * h.vz)

        solver.check()
        return sum(solver.model()[var].as_long() for var in [pxr, pyr, pzr])
