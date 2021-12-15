#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

"""Single fold."""

import sys
from functools import reduce

from pprint import pprint
from typing import List, Tuple

# f - (x - f) = f - x + f = 2f - x

Dot = Tuple[int, int]
Paper = List[Dot]


def max_tuple_values(acc: Dot, dot: Dot) -> Dot:
    return (
        max(acc[0], dot[0]),
        max(acc[1], dot[1]),
    )


def print_paper(paper: Paper) -> None:
    (max_x, max_y) = reduce(max_tuple_values, paper)

    dot_lookup = frozenset(paper)

    print("\u2508" * (max_x + 1))
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print('#' if (x, y) in dot_lookup else ' ', end='')
        print()


def fold_along_y(x: int, y: int, fold: int) -> Paper:
    return (
        x,
        y if y < fold else fold * 2 - y,
    )


def fold_along_x(x: int, y: int, fold: int) -> Paper:
    return (
        x if x < fold else 2 * fold - x,
        y,
    )


def main() -> None:
    dot_data, instructions = sys.stdin.read().strip().split("\n\n")

    dots: Paper = [
        tuple(int(value) for value in line.strip().split(","))
        for line in dot_data.split("\n")
    ]
    # print_paper(dots)

    handlers = {
        "fold along x": fold_along_x,
        "fold along y": fold_along_y,
    }

    for instruction in instructions.strip().split("\n"):
        print(repr(instruction))
        handler_name, fold = instruction.split("=")
        handler = handlers[handler_name]

        dots = list(set(handler(x, y, int(fold)) for x, y in dots))

        print(len(dots))

    print_paper(dots)


if __name__ == "__main__":
    main()
