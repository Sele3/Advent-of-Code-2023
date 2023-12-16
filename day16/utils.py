from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Represent the four directions as integers
U = 0
D = 1
L = 2
R = 3

# For each tile, we store the directions that can be reached from it
TILES = {
    ".": {U: [U], D: [D], L: [L], R: [R]},
    "/": {U: [R], D: [L], L: [D], R: [U]},
    "\\": {U: [L], D: [R], L: [U], R: [D]},
    "-": {U: [L, R], D: [L, R], L: [L], R: [R]},
    "|": {U: [U], D: [D], L: [U, D], R: [U, D]},
}
# For each direction, we store the offset to the next tile
OFFSETS = {
    U: (-1, 0),
    D: (1, 0),
    L: (0, -1),
    R: (0, 1),
}


@dataclass
class BeamGrid:
    """
    Represents a grid of tiles that can be traversed by a beam.
    """

    grid: List[str]

    def __post_init__(self):
        self.m = len(self.grid)
        self.n = len(self.grid[0])

    def count_energized_tiles(self, r: int, c: int, d: int) -> int:
        """
        Counts the number of tiles that can be reached from the initial tile (r, c) in direction d.
        :param r: The row of the initial tile
        :param c: The column of the initial tile
        :param d: The direction of the beam, one of U, D, L, R

        | Optimizations:
        | - We use a stack based DFS approach to avoid recursion
        | - We use a dictionary with (r, c) as keys and a bitmask for the seen directions as values.
            This can speed up computation as compared to using a set of (r, c, d) tuples.
        """
        stk: List[Tuple[int, int, int]] = [(r, c, d)]
        seen: Dict[Tuple[int, int], int] = defaultdict(int)

        while stk:
            r, c, d = stk.pop()
            if not (0 <= r < self.m and 0 <= c < self.n) or seen[(r, c)] & (1 << d):
                continue

            seen[(r, c)] |= 1 << d
            symbol = self.grid[r][c]

            for new_dir in TILES[symbol][d]:
                dr, dc = OFFSETS[new_dir]
                stk.append((r + dr, c + dc, new_dir))

        return len(seen.keys())
