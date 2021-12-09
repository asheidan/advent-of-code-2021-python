#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

from collections import namedtuple
from dataclasses import dataclass
from functools import reduce
import sys
from itertools import product
from typing import List, Tuple, Set
from pprint import pprint

@dataclass
class Position:
    x: int
    y: int

    def __str__(self) -> str:
        return f"<{self.x},{self.y}>"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Board:
    def __init__(self, board: str):
        self.board = board.strip().split("\n")

        self.max_y = len(self.board) - 1
        self.max_x = len(self.board[0]) - 1

        print(self.max_x, self.max_y)

    def is_lowpoint(self, x: int, y: int) -> bool:
        value = self.board[y][x]

        return all((
            y == 0 or (value < self.board[y - 1][x]),  # North
            y == self.max_y or (value < self.board[y + 1][x]),  # South
            x == 0 or (value < self.board[y][x - 1]),  # West
            x == self.max_x or (value < self.board[y][x + 1]),  # East
        ))

    def lowpoints(self) -> List[Position]:
        """Return the coordinates of the lowpoints."""

        return [
            Position(x, y)
            for x in range(self.max_x + 1)
            for y in range(self.max_y + 1)
            if self.is_lowpoint(x, y)
        ]

    def explore_basins(self):
        """Explore the basins."""

        # Remember to keep track of visited positions/positions part of any
        # basin in order to detect basins that have several lowpoints.
        print("-" * 90)

        basin_sizes = []

        visited: Set[Position] = set()
        for lowpoint in self.lowpoints():
            current_basin: Set[Position] = set()
            to_visit: Set[Position] = set()
            to_visit.add(lowpoint)

            while to_visit:
                visiting_position = to_visit.pop()

                visited.add(visiting_position)
                current_basin.add(visiting_position)

                directions = [
                    (-1, 0),
                    (+1, 0),
                    (0, -1),
                    (0, +1),
                ]

                for offset_x, offset_y in directions:
                    next_position = Position(visiting_position.x + offset_x,
                                             visiting_position.y + offset_y)

                    if next_position.x in range(0, self.max_x + 1) and next_position.y in range(self.max_y + 1):
                        if next_position not in visited:
                            if self.board[next_position.y][next_position.x] != "9":
                                # print(lowpoint, next_position, repr(self.board[next_position.y][next_position.x]))
                                to_visit.add(next_position)

                    # print(visiting_position, len(to_visit), len(current_basin), len(visited))

            basin_sizes.append(len(current_basin))
        
        basin_sizes.sort()
        print(basin_sizes[-3:])
        
        print(reduce((lambda acc, e: acc * e), basin_sizes[-3:], 1))


    def __str__(self) -> str:
        return "\n".join(self.board)


def main() -> None:
    board_data = sys.stdin.read()

    board = Board(board_data)
    print(board)
    basins = board.explore_basins()


if __name__ == "__main__":
    main()
