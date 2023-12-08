import re
from typing import Dict

from advent_of_code_solver import BaseSolver

from .utils import MultiStartNavigator, Node, SingleStartNavigator

NETWORK: Dict[str, Node] = {}


class Solver(BaseSolver):
    def parse_input(self, file):
        instructions, nodes = file.read().split("\n\n")

        # Construct the network dictionary
        for line in nodes.splitlines():
            name, left, right = re.findall(r"[A-Z]{3}", line)
            NETWORK[name] = Node(name, left, right)

        return instructions

    def solve_part1(self):
        navigator = SingleStartNavigator(self.input, NETWORK)
        return navigator.get_steps_to_reach()

    def solve_part2(self):
        nodes = list(NETWORK.keys())
        sources = [node for node in nodes if node[-1] == "A"]
        destinations = [node for node in nodes if node[-1] == "Z"]

        navigator = MultiStartNavigator(self.input, NETWORK, sources, destinations)
        return navigator.get_steps_to_reach()
