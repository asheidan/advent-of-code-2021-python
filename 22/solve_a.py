#!/usr/bin/env python3

import sys
import itertools
from typing import Iterator, Tuple

Position = Tuple[int, int, int]

MIN = -50
MAX = 50


def cuboid(start: Position, stop: Position) -> Iterator[Position]:
    end = tuple(map(lambda v: v + 1, stop))

    combined = zip(start, end)
    ranges = map(lambda pair: range(max(pair[0], MIN), min(pair[1], MAX)), combined)

    return itertools.product(*ranges)


def main() -> None:
    from pprint import pprint

    on = set()

    for line in sys.stdin.readlines():
        operation, coordinates = line.strip().split(" ")
        start, stop = zip(
            *(
                [int(v) for v in axis_range[2:].split("..")]
                for axis_range in coordinates.split(",")
            )
        )
        print(start, stop)
        operation_method = on.update if operation == "on" else on.difference_update
        operation_method(cuboid(start, stop))

        print(len(on))

    ##pprint(list(cuboid((0,0,0), (1,1,1))))


if __name__ == "__main__":
    main()
