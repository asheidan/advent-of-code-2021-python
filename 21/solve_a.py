#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

from itertools import repeat, islice


def deterministic_die(N):
    while True:
        yield from range(1, N + 1)


def main() -> None:
    player_count = 2
    scores = [0] * player_count
    player_positions = [0] * player_count
    player_positions = [4-1, 7-1]

    die = deterministic_die(100)

    roll_count = 0

    for current_round in range(1, 1000 + 1):
        for player in range(player_count):
            #print(f"{player} | p:{player_positions[player]+1} | s:{scores[player]}")
            rolls = list(islice(die, 3))
            roll_count += 3
            roll_sum = sum(rolls)

            # Move on the board
            player_positions[player] += roll_sum
            player_positions[player] %= 10

            # Update scores
            scores[player] += player_positions[player] + 1

            print(f"{player} | p:{player_positions[player]+1 : >2} | s:{scores[player] : >3}")

            if scores[player] >= 1000:
                break

        else:
            continue

        break
    
    print(scores[(player + 1) % 2], roll_count, scores[(player + 1) % 2] * roll_count)


if __name__ == "__main__":
    main()
