#!/usr/bin/env python3
"""How many times to the digits 1, 4, 7, and 8 occur in the output values."""

import sys


def main() -> None:

    count = 0

    for line in sys.stdin:
        _number_signals, output_signals = line.strip().split(" | ")

        outputs = output_signals.split(" ")

        count += sum(1 for signal in outputs if len(signal) in [2, 3, 4, 7])  # Number of segments for 1, 7, 4, 8

    print(count)

if __name__ == "__main__":
    main()
