#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import queue
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from math import inf
from typing import DefaultDict
from typing import Dict
from typing import FrozenSet
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

WORK_LOG = []
CURRENTLY_LOWEST = 9e999

COMPUTE_CACHE: Dict[Tuple[int, int], int] = {}
"""Lowest cost to reach position currently."""

BOARD = None
TARGET = None


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self) -> str:

        return f"<{self.x},{self.y}>"

    def __cmp__(self, other):
        return (self.x, self.y).__cmp__((other.x, other.y))

    def __lt__(self, other) -> bool:
        return (self.x, self.y) < (other.x, other.y)


class Board:

    def __init__(self, data: str, wraps: int = 5) -> None:
        self.board = [[int(v) - 1 for v in line] for line in data.strip().split("\n")]

        self.width = len(self.board[0])
        self.height = len(self.board)

        self.wraps = wraps


    def __len__(self) -> int:
        return self.width * self.height * self.wraps * self.wraps

    def __getitem__(self, key: Position) -> int:
        value = self.board[key.y % self.height][key.x % self.width]

        value = (value + key.x // self.width + key.y // self.height) % 9 + 1

        return value

    def __contains__(self, item: Position) -> bool:

        return item.x in range(self.width * self.wraps + 1) and item.y in range(self.height * self.wraps + 1)

    def maxposition(self) -> "Position":

        return Position(x=self.wraps * self.width - 1, y=self.wraps * self.height - 1)

    def naive_cost(self) -> int:
        return (sum(self[Position(x, 0)] for x in range(1, self.width * self.wraps))
                + sum(self[Position(0, y)] for y in range(1, self.height * self.wraps)))

    def adjacent(self, position: Position) -> Iterable[Position]:
        """Return iterable for adjacent nodes."""

        return [position + Position(*p)
                for p in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                if position + Position(*p) in self]


def dijkstra(board: Board, start: Position, target: Position) -> int:
    shortest_paths = defaultdict(
        lambda : inf,
        {
            start: 0,
        },
    )

    job_target = len(board)
    job_count = 0

    heap = queue.PriorityQueue()
    heap.put((0, start))

    while job := heap.get():
        cost, position = job
        job_count += 1

        if position == target:

            return cost

        if cost > shortest_paths[position]:

            continue

        for neighbour in board.adjacent(position):
            this_path_cost = cost + board[neighbour]

            if this_path_cost < shortest_paths[neighbour]:
                heap.put((this_path_cost, neighbour))
                shortest_paths[neighbour] = this_path_cost

    return -1


def main() -> None:
    board = Board(sys.stdin.read().strip())

    print(dijkstra(board, start=Position(0, 0), target=board.maxposition()))


if __name__ == "__main__":
    main()
