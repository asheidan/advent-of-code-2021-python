#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import itertools
import sys
from typing import List, Tuple, Optional

Board = List[List[int]]
Position = Tuple[int, int]


def next_step(board: Board) -> Board:
    next_board = [[n + 1 for n in line] for line in board]
    return next_board


def flash(x: int, y: int, board: Board):
    """Change the board only to increase the energy-levels correrctly."""

    flashed_area = filter(
        (lambda pos: pos[0] != x or pos[1] != y),
        itertools.product(
            range(max(0, x - 1), min(x + 2, len(board[0]))),
            range(max(0, y - 1), min(y + 2, len(board))),
        ),
    )
    for pos_x, pos_y in flashed_area:
        value = board[pos_y][pos_x]
        if value is not None:
            board[pos_y][pos_x] = value + 1

    board[y][x] = None


def flashes_on_board(board: Board) -> List[Position]:
    width = len(board[0])
    height = len(board)

    return [
        (x, y)
        for x, y, in itertools.product(range(width), range(height))
        if board[y][x] and board[y][x] > 9
    ]


def print_board(board: Board, turn: Optional[int] = None) -> None:
    return
    turn = "" if turn is None else turn
    print(f"\u250C\u2508\u2508{turn :^27}\u2508\u2508\u2510")
    print(
        "\u2502 "
        + " \u2502\n\u2502 ".join(
            " ".join(f"{'' if n is None else n : >2}" for n in line) for line in board
        )
        + " \u2502"
    )
    print("\u2514" + "\u2508" * 31 + "\u2518")


def main() -> None:
    board = [[int(n) for n in line.strip()] for line in sys.stdin]

    turns = 100

    flash_count = 0

    print_board(board, 0)

    for turn in range(1, turns + 1):
        board = next_step(board)
        print_board(board, str(turn) + "s")
        while flash_positions := flashes_on_board(board):
            for x, y in flash_positions:
                flash(x, y, board)
                flash_count += 1

        print_board(board, str(turn) + "e")

        board = [[0 if v is None else v for v in line] for line in board]

        print_board(board, str(turn) + "z")

    print(flash_count)

if __name__ == "__main__":
    main()
