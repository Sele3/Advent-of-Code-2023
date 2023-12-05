from bisect import bisect_right
from collections import deque
from dataclasses import dataclass, field
from functools import total_ordering
from typing import List, Optional


@total_ordering
@dataclass
class CategoryRange:
    """
    A range of values in the source category that maps to a range of values in the destination category.
    """

    dest_start: int
    src_start: int
    range_len: int

    # The range of values in the source category.
    src_range: range = field(init=False)

    def __post_init__(self):
        self.src_range = range(self.src_start, self.src_start + self.range_len)

    def map(self, value: int) -> int:
        """
        Maps a value from the source category to the destination category.
        """
        return self.dest_start + (value - self.src_start)

    def __lt__(self, other: "CategoryRange") -> bool:
        return self.src_start < other.src_start

    def __eq__(self, other: "CategoryRange") -> bool:
        return self.src_start == other.src_start


def combine_ranges(ranges: List[range]) -> List[range]:
    """
    Sorts and combines overlapping ranges.
    :param ranges: An unsorted list of ranges.
    :return: A sorted list of ranges with overlapping ranges combined.
    """
    ranges.sort(key=lambda r: r.start)
    stk = []

    for r in ranges:
        if stk and stk[-1].stop >= r.start:
            stk[-1] = range(stk[-1].start, max(stk[-1].stop, r.stop))
        else:
            stk.append(r)

    return stk


def create_full_category_range(
    category_ranges: List[CategoryRange],
) -> List[CategoryRange]:
    """
    Creates a full category range that covers the entire source category, from 0 to 9,999,999,999.
    :return: A sorted list of category ranges, with no gaps between them.
    """
    category_ranges.sort()
    result = []
    start = 0
    stop = 9_999_999_999

    for category_range in category_ranges:
        # Fill in the gap between the previous category range and the current category range.
        if start < category_range.src_start:
            result.append(CategoryRange(start, start, category_range.src_start - start))

        # Add the existing category range.
        result.append(category_range)
        # Update the start to the end of the current category range.
        start = category_range.src_range.stop

    result.append(CategoryRange(start, start, stop - start + 1))
    return result


class CategoryMapper:
    """
    A mapper that maps a value from the source category to the destination category.
    Uses the Chain of Responsibility design pattern.
    """

    def __init__(self, category_ranges: List[CategoryRange]):
        self.category_ranges = create_full_category_range(category_ranges)
        self.next_mapper: Optional[CategoryMapper] = None

    def set_next_mapper(self, next_mapper: "CategoryMapper") -> None:
        """
        Set the next mapper in the chain.
        """
        if self.next_mapper is None:
            self.next_mapper = next_mapper
        else:
            self.next_mapper.set_next_mapper(next_mapper)

    def map(self, value: int) -> int:
        """
        Maps a value from the source category to the destination category,
        then passes it to the next mapper in the chain.
        :param value: A value from the source category.
        :return: A value from the destination category.
        """
        category_range = self._find_category_range(value)
        new_value = category_range.map(value)

        return (
            self.next_mapper.map(new_value)
            if self.next_mapper is not None
            else new_value
        )

    def map_ranges(self, ranges: List[range]) -> List[range]:
        """
        Maps a list of ranges from the source category to the destination category,
        then passes it to the next mapper in the chain.
        :param ranges: A list of ranges from the source category.
        :return: A list of ranges from the destination category.
        """
        ranges = combine_ranges(ranges)
        queue = deque(ranges)
        mapped_ranges = []

        while queue:
            r = queue.popleft()

            category_range = self._find_category_range(r.start)

            # Get the smaller of the two stops.
            stop = min(r.stop, category_range.src_range.stop)

            mapped_start = category_range.map(r.start)
            mapped_stop = category_range.map(stop)
            mapped_ranges.append(range(mapped_start, mapped_stop))

            # Add the remaining range back to the queue if the seed range is larger than the category range.
            if stop < r.stop:
                queue.append(range(stop, r.stop))

        return (
            self.next_mapper.map_ranges(mapped_ranges)
            if self.next_mapper is not None
            else mapped_ranges
        )

    def _find_category_range(self, value: int) -> CategoryRange:
        """
        Finds the category range that contains the value.
        """
        idx = bisect_right(self.category_ranges, CategoryRange(0, value, 0)) - 1
        return self.category_ranges[idx]
