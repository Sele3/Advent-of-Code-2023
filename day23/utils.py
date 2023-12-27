from dataclasses import dataclass
from typing import Dict


@dataclass
class Coordinate:
    """
    Represents a coordinate in the grid, using complex numbers to represent the row and column
    """

    comp: complex

    def __post_init__(self):
        self.r = int(self.comp.real)
        self.c = int(self.comp.imag)

    def __eq__(self, other):
        return self.comp == other.comp

    def __hash__(self):
        return hash(self.comp)

    def __iter__(self):
        return iter((self.r, self.c))

    def __add__(self, other):
        return Coordinate(self.comp + other.comp)


class Graph:
    """
    Represents a graph, where each vertex is a coordinate in the grid
    """

    def __init__(self, g: Dict[Coordinate, Dict[Coordinate, int]]):
        self.g = g

    def get_longest_path(self, start: Coordinate, end: Coordinate) -> int:
        """
        Returns the length of the longest path from start to end
        """

        def dfs(curr: Coordinate, steps: int = 0) -> None:
            """
            Performs a DFS from curr to end, keeping track of the number of steps taken
            """
            # If we have reached the end, then we update the longest path
            if curr == end:
                nonlocal longest
                longest = max(longest, steps)
                return

            # Optimisation: If the end node is a neighbour of the current node, we can just go straight to it
            if end in self.g[curr]:
                dfs(end, steps + self.g[curr][end])
                return

            # Iterate through the neighbours of the current node and perform a DFS on them
            for neighbour, step in self.g[curr].items():
                if neighbour not in visited:
                    visited.add(neighbour)
                    dfs(neighbour, steps + step)
                    visited.remove(neighbour)

        longest = 0
        visited = set()
        dfs(start)
        return longest
