#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sys
from typing import List
from pprint import pprint


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

    def lowpoints(self) -> List[int]:
        """Return the risk levels for the lowpoints."""

        return [
            int(self.board[y][x]) + 1
            for x in range(self.max_x + 1)
            for y in range(self.max_y + 1)
            if self.is_lowpoint(x, y)
        ]

    def __str__(self) -> str:
        return "\n".join(self.board)


def main() -> None:
    board_data = sys.stdin.read()

    board = Board(board_data)
    print(board)
    lowpoints = board.lowpoints()
    print(sum(lowpoints))


if __name__ == "__main__":
    main()
