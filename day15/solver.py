from collections import defaultdict

from advent_of_code_solver import BaseSolver

TABLE_SIZE = 256


def custom_hash(s: str) -> int:
    """
    Executes the custom hash function on the given string.
    :return: An integer between 0 and 255.
    """
    curr = 0
    for c in s:
        curr += ord(c)
        curr *= 17
        curr %= 256

    return curr


def get_total_power(hm: dict) -> int:
    """
    Traverse the dictionary and compute the total power of the focal nodes.
    """
    return sum(idx * val for idx, val in enumerate(hm.values(), start=1))


class Solver(BaseSolver):
    def parse_input(self, file):
        return file.read().strip()

    def solve_part1(self):
        return sum(map(custom_hash, self.input.split(",")))

    def solve_part2(self):
        # Initialize the hash table.
        ht = [defaultdict(int) for _ in range(TABLE_SIZE)]

        for step in self.input.split(","):
            match step.strip("-").split("="):
                case [label]:  # Remove the focal node.
                    idx = custom_hash(label)
                    if label in ht[idx]:
                        del ht[idx][label]

                case [label, focal]:  # Insert the focal node.
                    idx = custom_hash(label)
                    ht[idx][label] = int(focal)

        return sum(idx * get_total_power(hm) for idx, hm in enumerate(ht, start=1))
