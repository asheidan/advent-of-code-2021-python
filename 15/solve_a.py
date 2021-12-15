#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys
from typing import Dict, List, Tuple, Optional, FrozenSet

Position = Tuple[int, int]
Board = List[str]


COMPUTE_CACHE: Dict[Tuple[int, int], int] = {}
"""Lowest cost to reach position currently."""


def explore(
    board: Board,
    position: Position,
    visited: FrozenSet[Position] = frozenset(),
    current_risk=0,
    currently_lowest=9e999,
) -> int:
    """Return the lowest risk to goal for position."""

    max_y = len(board) - 1
    max_x = len(board[0]) - 1

    current_x, current_y = position

    #print(position, currently_lowest, current_risk, visited)

    if current_risk >= currently_lowest:

        return currently_lowest

    if current_risk >= COMPUTE_CACHE.get(position, float('inf')):

        return currently_lowest

    else:
        COMPUTE_CACHE[position] = current_risk

    if position == (max_x, max_y):
        print("New lowest risk:", current_risk)

        return current_risk

    visited = visited | frozenset((position,))

    for step_x, step_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        next_x = current_x + step_x
        next_y = current_y + step_y

        next_position = (next_x, next_y)

        if all(
            (
                next_x in range(max_x + 1),
                next_y in range(max_y + 1),
                next_position not in visited,
            )
        ):

            score = explore(
                board=board,
                position=next_position,
                visited=visited,
                current_risk=current_risk + board[next_y][next_x],
                currently_lowest=currently_lowest,
            )

            if score < currently_lowest:
                #print("New lowest risk:", score)
                currently_lowest = score

    return currently_lowest


def dijkstra(board: Board) -> int:

    width = len(board[0])
    height = len(board)

    remaining = [(x, y) for x, y in itertools.product(range(width), range(height))]


def main() -> None:
    board = [[int(v) for v in line] for line in sys.stdin.read().strip().split("\n")]

    if len(board) < 20:
        from pprint import pprint
        pprint(board)

    print(explore(board=board, position=(0, 0)))


if __name__ == "__main__":
    main()
