#!/usr/bin/env python3

import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Iterator
from typing import Tuple

# pylint: disable=missing-function-docstring, missing-class-docstring


def unidirectional_range(a: int, b: int) -> range:
    step = 1 if (a <= b) else -1
    return range(a, b + step, step)


@dataclass
class Position:
    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __hash__(self) -> Tuple[int, int]:
        return hash((self.x, self.y))

    @classmethod
    def from_string(cls, input: str) -> "Position":
        return cls(*(int(coordinate) for coordinate in input.split(",")))


class Path:
    def __init__(self, start: Position, end: Position) -> None:
        self.start = start
        self.end = end

    def __iter__(self) -> Iterator[Position]:
        """Return Iterator over the positions in this Path.

        INCLUDE diagonal lines."""

        distance_x = self.end.x - self.start.x
        distance_y = self.end.y - self.start.y

        if distance_x:
            x_range = unidirectional_range(self.start.x, self.end.x)
        else:
            x_range = itertools.repeat(self.start.x)

        if distance_y:
            y_range = unidirectional_range(self.start.y, self.end.y)
        else:
            y_range = itertools.repeat(self.start.y)

        return (Position(x, y) for x, y in zip(x_range, y_range))

    def __str__(self) -> str:
        return f"{self.start} -> {self.end}"

    @classmethod
    def from_string(cls, input: str) -> "Path":
        return cls(*map(Position.from_string, input.strip().split(" -> ")))


def main() -> None:

    vent_paths = [Path.from_string(line) for line in sys.stdin]
    vent_map = defaultdict(int)

    for vent_path in vent_paths:
        print(f"### {vent_path}")
        for position in vent_path:
            if len(vent_paths) <= 10:
                print(f"### --- {position}")
            vent_map[position] += 1

    print(sum(1 for count in vent_map.values() if count >= 2))


if __name__ == "__main__":
    main()
