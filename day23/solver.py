from collections import deque
from typing import List

from advent_of_code_solver import BaseSolver

from .utils import Coordinate, Graph

DIRECTIONS = {
    "^": Coordinate(-1),
    "<": Coordinate(-1j),
    ">": Coordinate(1j),
    "v": Coordinate(1),
}


def create_graph(grid: List[str], ignore_slopes: bool = False) -> Graph:
    """
    Creates a graph from the input grid. The vertices are all the cells with 3 or more adjacent cells.
    :param grid: The input grid
    :param ignore_slopes: If True, the graph will ignore slopes and consider all adjacent cells as neighbours
    :return: A Graph object
    """

    def adjacent(coor: Coordinate) -> List[Coordinate]:
        """
        A helper function that returns a list of adjacent cells as Coordinate objects
        """
        adj = DIRECTIONS.values()

        # If ignore_slopes is False, then we fix its adjacent if the cell is a slope
        if not ignore_slopes and grid[coor.r][coor.c] in ("^", "<", ">", "v"):
            adj = [DIRECTIONS[grid[coor.r][coor.c]]]

        # Iterate through all the adjacent cells and check that they are in bounds and not walls
        result = []
        for d in adj:
            nr, nc = coor + d
            if nr in range(m) and nc in range(n) and grid[nr][nc] != "#":
                result.append(Coordinate(complex(nr, nc)))

        return result

    m, n = len(grid), len(grid[0])
    start, end = Coordinate(complex(1, 1)), Coordinate(complex(m - 2, n - 2))

    # Create a list of vertices
    vertices_list = [
        Coordinate(complex(r, c))
        for r in range(m)
        for c in range(n)
        if grid[r][c] == "." and len(adjacent(Coordinate(complex(r, c)))) > 2
    ] + [start, end]
    # Convert into a set
    vertices = set(vertices_list)

    # Create a graph from the vertices
    g = {v: {} for v in vertices}
    # For each vertex, do a BFS to find the distance to its neighbouring vertices
    for v in vertices:
        q = deque([(v, 0)])
        visited = {v}

        while q:
            curr, dist = q.popleft()

            # If the current cell is a vertex and not the original vertex, then we add it to the graph as a neighbour
            if curr in vertices and curr != v:
                g[v][curr] = dist
                continue

            # Otherwise, we continue the BFS
            for adj in adjacent(curr):
                if adj not in visited:
                    visited.add(adj)
                    q.append((adj, dist + 1))

    return Graph(g)


class Solver(BaseSolver):
    def parse_input(self, file):
        grid = file.read().splitlines()

        # Replace the entrance with a wall
        temp = list(grid[0])
        temp[1] = "#"
        grid[0] = "".join(temp)

        # Replace the exit with a wall
        temp = list(grid[-1])
        temp[-2] = "#"
        grid[-1] = "".join(temp)

        return grid

    def solve_part1(self):
        grid: List[str] = self.input
        m, n = len(grid), len(grid[0])
        start, end = Coordinate(complex(1, 1)), Coordinate(complex(m - 2, n - 2))

        return create_graph(grid).get_longest_path(start, end) + 2

    def solve_part2(self):
        # Takes 50 seconds to run, don't run unless you have to
        grid: List[str] = self.input
        m, n = len(grid), len(grid[0])
        start, end = Coordinate(complex(1, 1)), Coordinate(complex(m - 2, n - 2))

        return create_graph(grid, ignore_slopes=True).get_longest_path(start, end) + 2
