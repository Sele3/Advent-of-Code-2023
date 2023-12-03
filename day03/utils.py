from dataclasses import dataclass, field
from typing import List, Set, Tuple


@dataclass
class Schematic:
    grid: List[str]

    # Helper attributes
    m: int = field(init=False)  # Number of rows
    n: int = field(init=False)  # Number of columns
    seen: Set[Tuple[int, int]] = field(
        init=False, default_factory=set
    )  # Stores coordinates of parts that have been seen

    # Solution-specific attributes
    part_numbers: List[int] = field(init=False, default_factory=list)
    gear_ratios: List[int] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.m = len(self.grid)
        self.n = len(self.grid[0])

        self._process_grid()

    def _process_grid(self) -> None:
        """
        Processes the grid to find part numbers and gear ratios.

        | Algorithm:
        | 1. Iterate through the grid.
        | 2. If the current cell is a number or period (".") then skip it.
        | 3. If the current cell is a symbol, then add the part numbers of the adjacent cells to
             the list of part numbers.
        | 4. If the current cell is a gear ("*") and has exactly two adjacent cells that are part numbers,
             then add the product of the two part numbers to the list of gear ratios.
        """
        for r in range(self.m):
            for c in range(self.n):
                if self.grid[r][c] == "." or self.grid[r][c].isdigit():
                    continue

                curr_part_numbers = []
                for x, y in self._adjacent_coords(r, c):
                    if self.grid[x][y].isdigit() and (x, y) not in self.seen:
                        curr_part_numbers.append(self._construct_part_number(x, y))

                if len(curr_part_numbers) == 2 and self.grid[r][c] == "*":
                    self.gear_ratios.append(curr_part_numbers[0] * curr_part_numbers[1])

                self.part_numbers.extend(curr_part_numbers)

    def _adjacent_coords(self, r: int, c: int) -> List[Tuple[int, int]]:
        """
        Returns a list of coordinates adjacent to (r, c) that are within the grid, including diagonals.
        """
        return [
            (r + dr, c + dc)
            for dr in range(-1, 2)
            for dc in range(-1, 2)
            if (dr, dc) != (0, 0) and 0 <= r + dr < self.m and 0 <= c + dc < self.n
        ]

    def _construct_part_number(self, r: int, c: int) -> int:
        """
        Constructs the part number at (r, c) by finding the start and end of the part number.
        """
        start = end = c
        self.seen.add((r, c))

        while start > 0 and self.grid[r][start - 1].isdigit():
            start -= 1
            self.seen.add((r, start))

        while end + 1 < self.n and self.grid[r][end + 1].isdigit():
            end += 1
            self.seen.add((r, end))

        return int(self.grid[r][start : end + 1])
