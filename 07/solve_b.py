#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sys
import unittest
from collections import defaultdict
from typing import List


def print_graph(positions: List[int], file=sys.stdout) -> None:
    position_count = defaultdict(int)
    for position in positions:
        position_count[position] += 1

    min_cost = 9e100
    min_cost_position = -1
    for position in range(max(positions) + 1):
        cost = sum(
            cost_for_distance(abs(key - position)) * value
            for key, value in position_count.items()
            if key != position
        )

        if cost < min_cost:
            min_cost = cost
            min_cost_position = position

        print(
            # f"{p : >4} | {'-' * position_count[p] if p in position_count else '' : <10} | {cost}",
            f"{position : >4} | {cost}",
            file=file,
        )

    print(min_cost_position, min_cost)


def cost_for_distance(distance: int) -> int:
    """Return the calculated cost for distance.

    distance: 1 2 3 4
    cost:     1 3 5 9
    """

    return sum(range(distance + 1))


class TestCostForDistance(unittest.TestCase):
    def test_0_distance_should_cost_0(self):
        # Given
        distance = 0

        # When
        result = cost_for_distance(distance)

        # Then
        self.assertEqual(0, result)

    def test_1_distance_should_cost_1(self):
        # Given
        distance = 1

        # When
        result = cost_for_distance(distance)

        # Then
        self.assertEqual(1, result)

    def test_2_distance_should_cost_3(self):
        # Given
        distance = 2

        # When
        result = cost_for_distance(distance)

        # Then
        self.assertEqual(3, result)

    def test_example_distances_should_have_correct_cost(self):
        # Given
        examples = [
            #(start, end, cost),
            (16, 5, 66),
            (1, 5, 10),
            (2, 5, 6),
            (0, 5, 15),
            (4, 5, 1),
            (2, 5, 6),
            (7, 5, 3),
            (1, 5, 10),
            (2, 5, 6),
            (14, 5, 45),
        ]

        def distance(start, end) -> int:
            return abs(end - start)

        # When
        result = [cost_for_distance(distance(start, end)) for start, end, _cost in examples]

        # Then
        expected = [cost for _start, _end, cost in examples]
        self.assertEqual(expected, result)


def main() -> None:
    positions = [int(s) for s in sys.stdin.read().strip().split(",")]
    print_graph(positions)


if __name__ == "__main__":
    main()
