from collections import namedtuple
from itertools import cycle
from math import lcm
from typing import Dict, List

Node = namedtuple("Node", ("name", "left", "right"))


class SingleStartNavigator:
    """
    A class that navigates a network of nodes starting from a single source node.
    """

    def __init__(self, instructions: str, network: Dict[str, Node]):
        self.instructions = instructions
        self.network = network
        self.current_node = "AAA"

    def get_steps_to_reach(self) -> int:
        """
        Returns the number of steps required to reach the destination node.
        """
        for steps, direction in enumerate(cycle(self.instructions), start=1):
            self._update_node_position(direction)

            if self._has_reached_destination():
                return steps

    def _update_node_position(self, direction: str) -> None:
        """
        Updates the current node position based on the direction.
        :param direction: Either "L" or "R"
        """
        node = self.network[self.current_node]
        self.current_node = node.left if direction == "L" else node.right

    def _has_reached_destination(self) -> bool:
        """
        Returns True if the current node is the destination node.
        """
        return self.current_node == "ZZZ"


class MultiStartNavigator(SingleStartNavigator):
    """
    A class that navigates a network of nodes starting from multiple source nodes.
    """

    def __init__(
        self,
        instructions: str,
        network: Dict[str, Node],
        sources: List[str],
        destinations: List[str],
    ):
        super().__init__(instructions, network)
        self.sources = sources
        self.destinations = set(destinations)

    def get_steps_to_reach(self) -> int:
        """
        Returns the number of steps required for all source nodes to reach the destination nodes at the same time.
        The number of steps is the LCM of the number of steps required for each source node to reach the destination.
        """
        steps_list = []

        for source_node in self.sources:
            self.current_node = source_node
            steps = super().get_steps_to_reach()
            steps_list.append(steps)

        return lcm(*steps_list)

    def _has_reached_destination(self) -> bool:
        """
        Returns True if the current node is one of the destination nodes.
        """
        return self.current_node in self.destinations
