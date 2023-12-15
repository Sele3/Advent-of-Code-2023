from advent_of_code_solver import BaseSolver

from .utils import DoubleLinkedList

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


class Solver(BaseSolver):
    def parse_input(self, file):
        return file.read().strip()

    def solve_part1(self):
        return sum(map(custom_hash, self.input.split(",")))

    def solve_part2(self):
        # Initialize the hash table.
        ht = [DoubleLinkedList() for _ in range(TABLE_SIZE)]

        for step in self.input.split(","):
            if step[-1] == "-":  # Remove the focal node.
                label = step[:-1]
                idx = custom_hash(label)
                ht[idx].remove(label)

            else:  # Insert the focal node.
                label, focal = step.split("=")
                focal = int(focal)
                idx = custom_hash(label)
                ht[idx].insert(label, focal)

        return sum(idx * dll.get_total_power() for idx, dll in enumerate(ht, start=1))
