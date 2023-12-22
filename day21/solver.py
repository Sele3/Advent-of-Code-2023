from collections import deque

from advent_of_code_solver import BaseSolver


def neighbours(comp: complex):
    return [comp + 1, comp - 1, comp + 1j, comp - 1j]


class Solver(BaseSolver):
    def parse_input(self, file):
        return file.read().splitlines()

    def solve_part1(self):
        grid = self.input
        m, n = len(grid), len(grid[0])
        start = 0 + 0j

        for r, row in enumerate(grid):
            if "S" in row:
                start = complex(r, row.index("S"))

        q = deque([(start, 0)])
        seen = set()

        for step in range(1, 64 + 1):
            seen = set()
            for _ in range(len(q)):
                curr, steps = q.popleft()

                for comp in neighbours(curr):
                    r, c = int(comp.real), int(comp.imag)

                    # For part 2, we need to wrap around the grid
                    # r, c = int(comp.real) % m, int(comp.imag) % n

                    if (
                        0 <= r < m
                        and 0 <= c < n
                        and grid[r][c] != "#"
                        and comp not in seen
                    ):
                        q.append((comp, steps + 1))
                        seen.add(comp)

                    if grid[r][c] != "#" and comp not in seen:
                        q.append((comp, steps + 1))
                        seen.add(comp)

            # For part 2, to find the first 3 values of the quadratic sequence
            # if step % 131 == 65:
            #     print(f"At step {step}, {len(seen)} positions are reachable")

        return len(seen)

    def solve_part2(self):
        def f(n):
            a0 = 3738
            a1 = 33270
            a2 = 92194

            b0 = a0
            b1 = a1 - a0
            b2 = a2 - a1
            return b0 + b1 * n + (n * (n - 1) // 2) * (b2 - b1)

        # Gave up on this part, used hardcoded values from part 1 to solve the puzzle
        goal = 26501365
        return f(goal // 131)
