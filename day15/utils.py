from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class DoubleLinkedListNode:
    """
    Represents a focal node in a doubly linked list.
    """

    label: str
    value: int
    prev: Optional["DoubleLinkedListNode"] = field(init=False, default=None)
    next: Optional["DoubleLinkedListNode"] = field(init=False, default=None)

    def __eq__(self, other):
        return self.label == other.label and self.value == other.value


@dataclass
class DoubleLinkedList:
    """
    Implementation of a doubly linked list.
    """

    head: Optional[DoubleLinkedListNode] = field(init=False, default=None)
    tail: Optional[DoubleLinkedListNode] = field(init=False, default=None)

    # stores the mapping from label to node
    nodes: Dict[str, DoubleLinkedListNode] = field(init=False, default_factory=dict)

    def __post_init__(self):
        # We use dummy head and tail nodes to prevent the need for null checks at both ends of the list.
        self.head = DoubleLinkedListNode("dummy_head", -1)
        self.tail = DoubleLinkedListNode("dummy_tail", -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert(self, label: str, value: int) -> None:
        """
        If the node with the given label already exists, update its value.
        Otherwise, insert a new node with the given label and value at the end of the list.
        """
        if label in self.nodes:
            self.nodes[label].value = value
            return

        node = DoubleLinkedListNode(label, value)
        self.nodes[label] = node

        node.next = self.tail
        node.prev = self.tail.prev
        self.tail.prev = node
        node.prev.next = node

    def remove(self, label: str) -> None:
        """
        Remove the node with the given label from the list if it exists.
        """
        if label not in self.nodes:
            return

        node = self.nodes[label]
        node.next.prev = node.prev
        node.prev.next = node.next
        del self.nodes[label]

    def get_total_power(self) -> int:
        """
        Traverse the list and compute the total power of the focal nodes.
        """
        power, slot = 0, 1
        curr = self.head.next

        while curr != self.tail:
            power += slot * curr.value
            slot += 1
            curr = curr.next

        return power
