#!/usr/bin/env python3

import sys
import itertools
from typing import List
from typing import Optional
from typing import Tuple
from typing import Set


Number = int
Position = Tuple[int, int]

class BingoException(Exception):
    pass

class Board:
    def __init__(self, board: List[Number]) -> None:
        self.board: List[Number] = board

        self.width = 5
        self.height = 5

        self.marked: Set[Position] = set()

    def get(self, position: Position) -> Number:
        row, column = position
        return self.board[row * self.width + column]

    def find(self, number: Number) -> Optional[Position]:
        """Return (row, column) for given number.

        Raises exception if number isn't on the board.
        """
        result: Optional[Number] = None

        try:
            index = self.board.index(number)
            result = (index // self.width, index % self.width)
        except ValueError:
            pass

        return result

    def mark(self, number: Number) -> None:
        """Mark the given number and raise if Bingo."""
        position = self.find(number)
        if position is None:

            return

        self.marked.add(position)

        row, column = position

        row_positions = ((row, c) for c in range(self.width))
        column_positions = ((r, column) for r in range(self.height))

        checker = lambda positions: all((p in self.marked) for p in positions)

        if any(map(checker, [row_positions, column_positions])):

            raise BingoException()

    def unmarked_sum(self) -> Number:
        all_positions = itertools.product(range(self.width), range(self.height))
        return sum(
            self.get(position)
            for position in all_positions
            if position not in self.marked
        )

    def _position_as_str(self, position: Position) -> str:
        number = self.get(position)
        is_marked = position in self.marked
        marker = "\033[7m" if is_marked else ""

        return f"{marker}{number : >2}\033[0m"

    def __str__(self) -> str:
        """Beware, this outputs ansi escapes"""

        return "\n".join(
            " ".join(
                self._position_as_str((row, column)) for column in range(self.width)
            )
            for row in range(self.height)
        )


def main() -> None:
    boards: List[Board] = []

    draw_numbers: List[Number] = [int(n) for n in sys.stdin.readline().split(",")]
    print(draw_numbers)

    for board_data in sys.stdin.read().split("\n\n"):
        # print(repr(board_data))

        board_numbers = [int(n) for n in board_data.split()]
        # print(board_numbers)

        # Change board
        board = Board(board_numbers)
        boards.append(board)

    for number in draw_numbers:
        print(f"--- {number : >2} ----------------------")
        try:
            for board in boards:
                board.mark(number)
                # print(board)
                # print()
        except BingoException:
            print("WINNER")
            print(board)

            unmarked_sum = board.unmarked_sum()
            print(f"### num: {number : >2} | sum: {unmarked_sum} | pro: {unmarked_sum * number} ###")

            break


if __name__ == "__main__":
    main()
