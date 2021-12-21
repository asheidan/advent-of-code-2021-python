#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

from itertools import repeat, islice
from typing import Tuple

COMPUTE_CACHE = {}


def dirac_round(player=0, positions=(0, 0), scores=(0, 0)) -> Tuple[int, int]:
    possible_rolls = [
        (3, 1),
        (4, 3),
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1),
    ]

    wins = [0, 0]

    for roll, multiplier in possible_rolls:
        position = (positions[player] + roll) % 10
        score = scores[player] + position + 1

        if score >= 21:
            wins[player] += multiplier
        else:
            next_player = int(not player)

            next_positions = (
                (position,) * next_player
                + positions[next_player : next_player + 1]
                + (position,) * player
            )
            next_scores = (
                (score,) * next_player
                + scores[next_player : next_player + 1]
                + (score,) * player
            )

            cached_wins = COMPUTE_CACHE.get((next_player, next_positions, next_scores))
            sub_wins = cached_wins or dirac_round(
                player=next_player, positions=next_positions, scores=next_scores
            )

            for p in range(2):
                wins[p] += multiplier * sub_wins[p]

    result = tuple(wins)
    COMPUTE_CACHE[(player, positions, scores)] = result
    return result


def main() -> None:

    wins = dirac_round(positions=(4 - 1, 8 - 1))
    print(wins, max(wins))
    print(len(COMPUTE_CACHE))


if __name__ == "__main__":
    main()
