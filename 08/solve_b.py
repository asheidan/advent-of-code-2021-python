#!/usr/bin/env python3
"""Determine how the wires are crossed for each entry."""

import sys
import unittest
from typing import List, Dict

[
    (0, "abcefg"),
    (1, "cf"),
    (2, "acdeg"),
    (3, "acdfg"),
    (4, "bcdf"),
    (5, "abdfg"),
    (6, "abdefg"),
    (7, "acf"),
    (8, "abcdefg"),
    (9, "abcdfg"),
]

def to_key(signals: str) -> str:
    return "".join(sorted(signals))


def parse_number_signals(signals: List[str]):
    # By finding the signals for 1 and 7 we can lock down the signal for the A-segment

    signals.sort(key=len)

    one_signals, seven_signals, four_signals, *signals = signals

    eight_signals = signals.pop()

    # Split by length
    two_three_five, six_nine_zero = signals[:-3], signals[-3:]

    # 3
    three_signals, = [signal for signal in two_three_five if not set(one_signals) - set(signal)]
    two_three_five.remove(three_signals)

    # 9
    nine_signals, = [signal for signal in six_nine_zero if not set(three_signals) - set(signal)]
    six_nine_zero.remove(nine_signals)

    # 6
    six_signals, = [signal for signal in six_nine_zero if set(one_signals) - set(signal)]
    six_nine_zero.remove(six_signals)

    # 0, should be the only one left of this length
    zero_signals, = six_nine_zero

    # 2
    two_signals, = [signal for signal in two_three_five if set(signal) - set(six_signals)]
    two_three_five.remove(two_signals)

    # 5, should be the only one left of this length
    five_signals, = two_three_five

    ordered_signals = [
            zero_signals,
            one_signals,
            two_signals,
            three_signals,
            four_signals,
            five_signals,
            six_signals,
            seven_signals,
            eight_signals,
            nine_signals,
            ]

    mapping: Dict[str, int] = {to_key(key): value for value, key in enumerate(ordered_signals)}

    # reverse_mapping = {v: k for k, v in mapping.items()}
    # for i in range(10):
    #     print(i, reverse_mapping[i])

    return mapping


def line_to_number(line: str) -> int:
    number_signals, output_signals = [group.split(" ") for group in line.strip().split(" | ")]

    mapping = parse_number_signals(number_signals)

    number = sum([mapping[to_key(signal)] * (10 ** base)
              for base, signal in enumerate(reversed(output_signals))])

    return number


def main() -> None:

    line_sum = 0

    for line in sys.stdin:
        line = line.strip()

        number = line_to_number(line)

        line_sum += number

        print(f"{line : <90} | {number : >4}")

    print("-" * 90 + "-+-----")
    print(f"{line_sum : >97}")


if __name__ == "__main__":
    main()


class TestLineToNumber(unittest.TestCase):

    def test_example_line_1625(self):
        # Given
        line = "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef"

        # When
        result = line_to_number(line)

        # Then
        self.assertEqual(1625, result)
