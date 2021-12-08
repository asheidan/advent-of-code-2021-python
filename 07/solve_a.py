#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sys
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
            abs(key - position) * value
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


def main() -> None:
    positions = [int(s) for s in sys.stdin.read().strip().split(",")]
    print_graph(positions)


if __name__ == "__main__":
    main()
