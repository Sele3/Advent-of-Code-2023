from dataclasses import dataclass
from heapq import heappop, heappush
from typing import List

# Represent the four directions as integers
U = 0
L = 1
D = 2
R = 3

# For each direction, we store the offset to the next tile
OFFSETS = {
    U: (-1, 0),
    D: (1, 0),
    L: (0, -1),
    R: (0, 1),
}


@dataclass
class CityMap:
    """
    Represents a map of cities that can be traversed by the crucible.
    """

    grid: List[List[int]]

    def __post_init__(self):
        self.m = len(self.grid)
        self.n = len(self.grid[0])

    def is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.m and 0 <= c < self.n

    def is_goal(self, r: int, c: int) -> bool:
        return r == self.m - 1 and c == self.n - 1

    def get_least_incurred_loss(self, min_steps: int, max_steps: int) -> int:
        """
        Returns the least incurred loss when traversing the map from (0, 0) to (m - 1, n - 1).
        Uses Uniform Cost Search (UCS) to find the least cost path.
        :param min_steps: The minimum number of steps to travel in a single direction
        :param max_steps: The maximum number of steps to travel in a single direction
        """
        seen = set()
        heap = [(0, 0, 0, -1)]

        while heap:
            # cost: The cost incurred so far
            # r, c: The current position
            # d: The direction we are currently facing
            cost, r, c, d = heappop(heap)

            if (r, c, d) in seen:
                continue

            if self.is_goal(r, c):
                return cost

            seen.add((r, c, d))
            for nd in range(4):  # nd: New direction
                # Skip the current direction and the opposite direction
                if d == nd or (d + 2) % 4 == nd:
                    continue

                add_cost = 0
                # step: Number of steps to travel in the same direction
                for step in range(1, max_steps + 1):
                    nr, nc = r + OFFSETS[nd][0] * step, c + OFFSETS[nd][1] * step
                    # If the new position is invalid, we break out of the loop
                    if not self.is_valid(nr, nc):
                        break

                    add_cost += self.grid[nr][nc]
                    # Add the new position to the heap only if the number of steps >= min_steps
                    # and the new position has not been visited
                    if step >= min_steps and (nr, nc, nd) not in seen:
                        heappush(heap, (cost + add_cost, nr, nc, nd))
