import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


@dataclass
class Part:
    """
    Represents a machine part with 4 attributes.
    """

    x: int
    m: int
    a: int
    s: int

    def __radd__(self, other):
        """
        Allows calling sum() on parts
        """
        return self.x + self.m + self.a + self.s + other

    def __iter__(self):
        """
        Allows tuple unpacking of a part
        """
        return iter((self.x, self.m, self.a, self.s))


@dataclass
class PartMap:
    """
    Represents a map of ranges for each attribute of a part.
    """

    x: range
    m: range
    a: range
    s: range

    def __getitem__(self, item) -> range:
        """
        Allows accessing the range of a particular attribute by name.
        """
        return getattr(self, item)

    def __setitem__(self, key, value):
        """
        Allows setting the range of a particular attribute by name.
        :param key: The name of the attribute
        :param value: The new range
        """
        setattr(self, key, value)

    @property
    def combinations(self) -> int:
        """
        Calculates the number of combinations that this part map represents.
        """
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


@dataclass
class Rule:
    """
    Represents a rule with a condition and a result.
    """

    condition: str
    result: str

    def partition(self, part_map: PartMap) -> Tuple[PartMap, PartMap]:
        """
        Partitions the part map into two parts based on the condition of this rule.
        The first part contains the ranges that satisfy the condition, the second part contains its complement.
        :return: A tuple of (satisfying_part_map, complement_part_map)
        """
        complement = deepcopy(part_map)
        attr, comparator, value = re.match(r"(\w)([<>])(\d+)", self.condition).groups()

        attr_range = part_map[attr]
        value = int(value)
        start, stop = attr_range.start, attr_range.stop

        if comparator == "<":
            part_map[attr] = range(start, value)
            complement[attr] = range(value, stop)
        else:
            part_map[attr] = range(value + 1, stop)
            complement[attr] = range(start, value + 1)

        return part_map, complement


@dataclass
class Workflow:
    """
    Represents a workflow with a name, a list of conditioned rules, and a default rule.
    """

    name: str
    rules: List[Rule]
    default_rule: Rule

    def evaluate(self, part: Part) -> str:
        """
        Evaluates the part against the rules of this workflow.
        :return: The name of the next workflow that first satisfies the rule condition.
        """
        x, m, a, s = part
        for rule in self.rules:
            if eval(rule.condition, {"x": x, "m": m, "a": a, "s": s}):
                return rule.result
        return self.default_rule.result

    def partition(self, part_map: PartMap) -> Iterable[Tuple[PartMap, str]]:
        """
        Iterate through the rules and partition the part map into its satisfying and complement parts.
        Then, yields the satisfying part map and the name of the next workflow.
        """
        for rule in self.rules:
            part_map, complement = rule.partition(part_map)
            yield part_map, rule.result
            part_map = complement

        yield part_map, self.default_rule.result


# Constants for the workflow names
START_WORKFLOW = "in"
ACCEPTED_WORKFLOW = "A"
REJECTED_WORKFLOW = "R"


class WorkflowHandler:
    """
    A handler for the list of workflows.
    """

    def __init__(self, workflows: List[Workflow]):
        self.map: Dict[str, Workflow] = {
            workflow.name: workflow for workflow in workflows
        }

    def evaluate_part(self, part: Part, workflow_name: str = START_WORKFLOW) -> bool:
        """
        Evaluates the part against the workflows and returns whether it is accepted or rejected.
        """
        if workflow_name == ACCEPTED_WORKFLOW:
            return True
        if workflow_name == REJECTED_WORKFLOW:
            return False

        new_workflow = self.map[workflow_name].evaluate(part)
        return self.evaluate_part(part, new_workflow)

    def count_accepted_combinations(
        self, part_map: PartMap, workflow_name: str = START_WORKFLOW
    ) -> int:
        """
        Counts the number of combinations that will be accepted by the workflows.
        """
        if workflow_name == ACCEPTED_WORKFLOW:
            return part_map.combinations
        if workflow_name == REJECTED_WORKFLOW:
            return 0

        result = 0
        for part_map, new_workflow in self.map[workflow_name].partition(part_map):
            result += self.count_accepted_combinations(part_map, new_workflow)

        return result
