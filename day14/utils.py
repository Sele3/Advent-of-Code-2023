from copy import deepcopy
from dataclasses import dataclass, field
from itertools import count
from typing import List


def tilt_north(grid: List[List[str]]) -> List[List[str]]:
    """
    Tilt the grid north, i.e. all the "O"s fall to the top of the grid.
    """

    grid = deepcopy(grid)
    m, n = len(grid), len(grid[0])

    for c in range(n):
        # Two pointers: bot is the bottom pointer, and r is the top pointer.
        bot = m - 1
        cnt = 0
        for r in range(m - 1, -1, -1):
            if grid[r][c] == ".":
                # Top pointer is at an empty space, continue execution.
                continue

            if grid[r][c] == "O":
                # Top pointer is at an "O", increment the counter and continue execution.
                cnt += 1
                continue

            # The top pointer is at an "#", move the bottom pointer.
            while bot > r:
                # Move the bottom pointer up and fill the empty spaces with "O"s if the distance between the top and
                # bottom pointers is less than or equal to the number of "O"s.
                grid[bot][c] = "O" if bot - r <= cnt else "."
                bot -= 1

            # Move the bottom pointer above the current pointer and clear the counter.
            bot -= 1
            cnt = 0

        # Continue moving the bottom pointer until it reaches the top of the grid.
        while bot >= 0:
            grid[bot][c] = "O" if bot < cnt else "."
            bot -= 1

    return grid


def get_total_load(grid: List[List[str]]) -> int:
    """
    Calculate the total load on the north support beams. We use a rotation on the grid to calculate row by row instead.
    """
    grid = rotate_clockwise(grid)
    return sum(
        idx for row in grid for idx, val in enumerate(row, start=1) if val == "O"
    )


def rotate_clockwise(grid: List[List[str]]) -> List[List[str]]:
    """
    Rotate the grid clockwise. This is done by transposing the grid and then reversing each row.
    """
    transposed = list(map(list, zip(*grid)))
    return [row[::-1] for row in transposed]


@dataclass
class State:
    """
    A state of the grid. We use a token to keep track of the state's position in the cycle.
    """

    # A unique token for each state, starting from 0.
    token: int = field(init=False, default_factory=count().__next__)
    grid: List[List[str]]

    # Cache the string representation of the grid.
    str_cache: str = field(init=False, default="")

    def __str__(self):
        if not self.str_cache:
            self.str_cache = "\n".join(map("".join, self.grid))
        return self.str_cache

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def cycle(self) -> "State":
        """
        Tilts the grid north, west, south, and east, which forms a cycle.
        :return:
        """
        grid = self.grid
        for _ in range(4):
            # We tilt the grid north, then rotate it clockwise, which is equivalent to tilting the grid anticlockwise.
            grid = tilt_north(grid)
            grid = rotate_clockwise(grid)

        return State(grid)
